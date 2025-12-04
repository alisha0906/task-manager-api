# tests/test_tasks.py

import pytest
import json
import uuid  # Required to generate unique usernames
from app import create_app
from models import db, User, Task

# --- Fixtures (Setup/Teardown) ---

@pytest.fixture
def app():
    # 1. Setup for testing: Create the app instance
    app = create_app()
    app.config.update({
        "TESTING": True,
        # Use an in-memory SQLite database for fast, isolated tests
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:", 
        "JWT_SECRET_KEY": "test-key" # Use a known key for testing
    })
    
    # 2. Application Context and Database Setup
    with app.app_context():
        # db.create_all() must be called inside the app context
        db.create_all()
        yield app
        # 3. Teardown: Clean up the database after tests
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    # Returns a test client for making HTTP requests
    return app.test_client()

@pytest.fixture
def auth_tokens(app):
    # Creates a user and logs them in, returning the necessary JWT token/headers
    with app.app_context():
        # FIX for IntegrityError: Generate a unique username for each fixture run
        unique_username = f'testuser_{uuid.uuid4().hex}' 
        
        # Create a test user with the unique name
        user = User(username=unique_username, password='testpassword')
        db.session.add(user)
        db.session.commit()
        
        # Login data
        login_data = {
            "username": unique_username, # Use the unique name for login
            "password": "testpassword"
        }
        
        client = app.test_client()
        response = client.post('/auth/login', json=login_data)
        
        # Ensure login was successful
        assert response.status_code == 200
        data = response.get_json()
        
        return {
            'headers': {'Authorization': f'Bearer {data["access_token"]}'},
            'user_id': user.id
        }

# --- Task CRUD Tests ---

def test_task_creation(app, auth_tokens):
    client = app.test_client()
    headers = auth_tokens['headers']
    
    # POST /tasks
    response = client.post(
        '/tasks/',
        headers=headers,
        json={'title': 'Test Task', 'description': 'Description for test task', 'completed': False}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Task'
    assert data['user_id'] == auth_tokens['user_id']
    
def test_task_list_and_filtering(app, auth_tokens):
    client = app.test_client()
    headers = auth_tokens['headers']
    
    # Create multiple tasks
    with app.app_context():
        db.session.add_all([
            Task(title='Task 1', description='Desc 1', completed=False, user_id=auth_tokens['user_id']),
            Task(title='Task 2', description='Desc 2', completed=True, user_id=auth_tokens['user_id'])
        ])
        db.session.commit()
    
    # GET /tasks (all)
    response = client.get('/tasks/', headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['tasks']) == 2 # Check count
    
    # GET /tasks (filtering completed=true - Bonus)
    response_filter = client.get('/tasks/?completed=true', headers=headers)
    data_filter = response_filter.get_json()
    assert len(data_filter['tasks']) == 1
    assert data_filter['tasks'][0]['title'] == 'Task 2'
    
def test_task_update(app, auth_tokens):
    client = app.test_client()
    headers = auth_tokens['headers']
    
    # Create a task to be updated
    with app.app_context():
        task = Task(title='Old Title', description='Old Desc', completed=False, user_id=auth_tokens['user_id'])
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        
    # PUT /tasks/{id}
    update_data = {'title': 'New Title', 'completed': True}
    response = client.put(f'/tasks/{task_id}', headers=headers, json=update_data)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'New Title'
    assert data['completed'] == True
    
def test_task_deletion(app, auth_tokens):
    client = app.test_client()
    headers = auth_tokens['headers']
    
    # Create a task to be deleted
    with app.app_context():
        task = Task(title='To Delete', description='Will be gone', user_id=auth_tokens['user_id'])
        db.session.add(task)
        db.session.commit()
        task_id = task.id
        
    # DELETE /tasks/{id}
    response = client.delete(f'/tasks/{task_id}', headers=headers)
    assert response.status_code == 200
    
    # Verify deletion (GET should fail with 404)
    response_check = client.get(f'/tasks/{task_id}', headers=headers)
    assert response_check.status_code == 404

# --- Authentication/Authorization Tests ---

def test_unauthenticated_access(client):
    # GET /tasks without a token
    response = client.get('/tasks/')
    assert response.status_code == 401 # Unauthorized
    
def test_task_unauthorized_access(app, auth_tokens):
    client = app.test_client()
    headers = auth_tokens['headers']
    
    # Create a task for a DIFFERENT user (ID 99)
    with app.app_context():
        task_other = Task(title='Other User Task', description='Should not be accessible', user_id=99)
        db.session.add(task_other)
        db.session.commit()
        task_id = task_other.id
        
    # Attempt to GET another user's task
    response_get = client.get(f'/tasks/{task_id}', headers=headers)
    assert response_get.status_code == 403 # Forbidden
    
    # Attempt to DELETE another user's task
    response_delete = client.delete(f'/tasks/{task_id}', headers=headers)
    assert response_delete.status_code == 403 # Forbidden