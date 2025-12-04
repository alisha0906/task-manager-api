# 🚀 Task Manager RESTful API (Flask + JWT)

This is a RESTful API for a simple task manager application built with **Flask**, **Flask-SQLAlchemy**, and **JWT** (JSON Web Token) authentication.

### ✨ Features Implemented

* **Core CRUD:** Full Create, Read, Update, and Delete operations on tasks.
* **User Authentication:** Secure registration and login using **JWT**.
* **Authorization:** Tasks are linked to users; users can only manage their own tasks.
* **Bonus 1: Filtering:** Tasks can be filtered by `completed` status (`GET /tasks?completed=true`).
* **Bonus 2: Pagination:** Task lists are paginated (`GET /tasks?page=1&per_page=10`).

---

## 🛠️ 1. Setup and Installation Guide

Follow these steps precisely to set up and run the application.

1.  **Clone the Repository and Navigate:**
    ```bash
    git clone <your_github_repo_link>
    cd task-manager-api
    ```

2.  **Create and Activate Virtual Environment:**
    * **Windows (PowerShell/CMD):**
        ```powershell
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * **macOS/Linux (Bash):**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Environment Variables & Secrets:**
    * Create a file named **`.env`** in the root directory and add your secret key:
        ```
        # .env
        JWT_SECRET_KEY="your_secure_random_jwt_secret_key"
        ```
    * Set the application entry point (needed for Flask commands):
        ```powershell
        $env:FLASK_APP="app:create_app"
        ```

5.  **Initialize Database Schema:**
    Run these commands to create the `app.db` file and the necessary `user` and `task` tables.
    ```bash
    flask db init
    flask db migrate -m "Initial task and user models"
    flask db upgrade
    ```

6.  **Run the Application:**
    ```powershell
    flask run
    ```
    The API will be available at `http://127.0.0.1:5000/`.

---

## 📜 2. API Documentation and Examples

| Endpoint | Method | Description | Authentication |
| :--- | :--- | :--- | :--- |
| `/auth/register` | `POST` | Create a new user account. | No |
| `/auth/login` | `POST` | Log in and receive an access token. | No |
| `/tasks` | `GET` | Get a list of tasks (supports **pagination** & **filtering**). | Yes |
| `/tasks` | `POST` | Create a new task. | Yes |
| `/tasks/<id>` | `GET` | Get details of a specific task. | Yes |
| `/tasks/<id>` | `PUT` | Update a task. | Yes |
| `/tasks/<id>` | `DELETE` | Delete a task. | Yes |

### Authentication Flow

### 1. Register User

**Request:**
```http
POST /auth/register
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}
```
Response (201 Created)
```json
{
    "msg": "User created successfully"
}
```

## 2. Login (Get JWT Token)
Request
```http
POST /auth/login
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}
```
Response (200 OK)
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Copy this token and include it in the Authorization header:
Authorization: Bearer <access_token>

## 📝 Task CRUD Examples
(Requires Authorization: Bearer <access_token>)
### 3. Create Task — POST /tasks
Request
```http
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Finalize Submission",
    "description": "Verify all tests pass and README is complete.",
    "completed": false
}
```
Response (201 Created)
```json
{
    "id": 1,
    "title": "Finalize Submission",
    "completed": false,
    "user_id": 1
}
```
### 4. Retrieve All Tasks — GET /tasks
This example demonstrates the Read operation and the Pagination/Filtering bonus features.

Request (Example with filtering):

```HTTP

GET /tasks?completed=false&page=1&per_page=10
Authorization: Bearer <access_token>
```
Response (200 OK):
```JSON

{
    "tasks": [
        {
            "id": 1,
            "title": "Finalize Submission",
            "...": "..."
        }
    ],
    "total_tasks": 1,
    "total_pages": 1,
    "current_page": 1
}
```
### 5. Update Task — PUT /tasks/{id}
Request (Update Task ID 1):

```HTTP
PUT /tasks/1
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Assignment Submitted",
    "completed": true
}
```
Response (200 OK):
```JSON
{
    "id": 1,
    "title": "Assignment Submitted",
    "completed": true,
    "user_id": 1,
    "...": "..."
}
```
### 6. Delete Task — DELETE /tasks/{id}
Request (Delete Task ID 1):

```HTTP
DELETE /tasks/1
Authorization: Bearer <access_token>
```
Response (200 OK):

```JSON
{
    "msg": "Task deleted successfully"
}
```
## 🧪 3. Testing

A. Unit Test Execution
This project includes unit tests (tests/test_tasks.py) that cover all endpoints and authorization logic.

1. Stop the running server.
2. Set Python Path (required for module discovery):
```powershell
$env:PYTHONPATH="."
```
3. Run Pytest
```bash
pytest tests/
```

Expected Output:  7 passed in X.XXs
