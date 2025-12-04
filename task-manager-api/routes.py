# routes.py

from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Helper function for input validation
def validate_task_data(data, is_new=True):
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed')

    if is_new and (not title or not description):
        return None, "Title and description are required."
    
    if completed is not None and not isinstance(completed, bool):
        return None, "Completed must be a boolean."

    return {
        'title': title,
        'description': description,
        'completed': completed
    }, None

# GET /tasks: Retrieve a list of all tasks (with pagination and filtering)
@tasks_bp.route('/', methods=['GET'])
@jwt_required()
def list_tasks():
    # FIX: Convert identity to integer
    current_user_id = int(get_jwt_identity()) 

    # 1. Base Query: Only tasks belonging to the current user
    query = Task.query.filter_by(user_id=current_user_id)

    # 2. Filtering (Bonus): Filter by completed status
    completed_status = request.args.get('completed', type=str)
    if completed_status is not None:
        if completed_status.lower() == 'true':
            query = query.filter_by(completed=True)
        elif completed_status.lower() == 'false':
            query = query.filter_by(completed=False)

    # 3. Pagination (Bonus)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginated_tasks = query.paginate(page=page, per_page=per_page, error_out=False)

    tasks_data = [task.to_dict() for task in paginated_tasks.items]

    return jsonify({
        'tasks': tasks_data,
        'total_tasks': paginated_tasks.total,
        'total_pages': paginated_tasks.pages,
        'current_page': paginated_tasks.page,
        'per_page': paginated_tasks.per_page
    })

# GET /tasks/{id}: Retrieve details of a specific task.
@tasks_bp.route('/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    # FIX: Convert identity to integer
    current_user_id = int(get_jwt_identity())
    
    # Retrieve task and ensure it belongs to the current user
    task = db.get_or_404(
        Task, 
        task_id, 
        description=f"Task with id {task_id} not found or doesn't belong to the user."
    )
    
    if task.user_id != current_user_id:
        # Prevent accessing tasks that belong to other users
        abort(403, description="You do not have permission to view this task.") 
        
    return jsonify(task.to_dict())

# POST /tasks: Create a new task.
@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    validated_data, error = validate_task_data(data, is_new=True)

    if error:
        return jsonify({"msg": error}), 400

    # FIX: Convert identity to integer
    current_user_id = int(get_jwt_identity())
    
    # Create the task, linking it to the authenticated user
    new_task = Task(
        title=validated_data['title'],
        description=validated_data['description'],
        user_id=current_user_id
    )
    
    # Check for optional 'completed' field in POST request
    if validated_data['completed'] is not None:
        new_task.completed = validated_data['completed']

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify(new_task.to_dict()), 201

# PUT /tasks/{id}: Update details of a specific task.
@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    data = request.get_json()
    # FIX: Convert identity to integer
    current_user_id = int(get_jwt_identity())
    
    task = db.get_or_404(Task, task_id)

    # Authorization Check: Ensure the task belongs to the user
    if task.user_id != current_user_id:
        abort(403, description="You do not have permission to edit this task.")

    validated_data, error = validate_task_data(data, is_new=False)
    
    if error:
        return jsonify({"msg": error}), 400
        
    # Update fields if they are provided in the request body
    if validated_data['title']:
        task.title = validated_data['title']
    if validated_data['description']:
        task.description = validated_data['description']
    if validated_data['completed'] is not None:
        task.completed = validated_data['completed']
        
    db.session.commit()
    return jsonify(task.to_dict())

# DELETE /tasks/{id}: Delete a specific task.
@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    # FIX: Convert identity to integer
    current_user_id = int(get_jwt_identity())

    task = db.get_or_404(Task, task_id)

    # Authorization Check: Ensure the task belongs to the user
    if task.user_id != current_user_id:
        abort(403, description="You do not have permission to delete this task.")

    db.session.delete(task)
    db.session.commit()
    
    return jsonify({'msg': 'Task deleted successfully'}), 200