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

#### 1. Register User

**Request:**
```http
POST /auth/register
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}

🔐 Authentication Flow
1. Register User
Request
POST /auth/register
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}

Response (201 Created)
{
    "msg": "User created successfully"
}

2. Login (Get JWT Token)
Request
POST /auth/login
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}

Response (200 OK)
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}


Copy this token and include it in the Authorization header:

Authorization: Bearer <access_token>

📝 Task CRUD Examples
(Requires Authorization: Bearer <access_token>)
3. Create Task — POST /tasks
Request
POST /tasks
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "title": "Finalize Submission",
    "description": "Verify all tests pass and README is complete.",
    "completed": false
}

Response (201 Created)
{
    "id": 1,
    "title": "Finalize Submission",
    "completed": false,
    "user_id": 1
}

🧪 3. Testing

Your project includes full unit tests for all endpoints.

A. Stop the Server

Press:

Ctrl + C

B. Set Python Path

(Required for module discovery)

$env:PYTHONPATH="."

C. Run Pytest
pytest tests/


Expected Output:

7 passed in X.XXs

📂 4. Project Structure
task-manager-api/
├── app.py              # Main Flask app, context, and blueprint registration
├── config.py           # Application configuration and JWT settings
├── models.py           # Database Models (User, Task)
├── auth.py             # User authentication routes
├── routes.py           # Task CRUD endpoints
├── tests/
│   └── test_tasks.py   # Unit tests for API endpoints
├── .env                # Environment variables
└── requirements.txt    # Project dependencies
