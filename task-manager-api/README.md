# 🚀 Task Manager RESTful API (Flask)

This is a RESTful API for a simple task manager application built with Flask, Flask-SQLAlchemy, and JWT-based authentication.

## ✨ Features

- **Task CRUD:** Create, Read, Update, Delete tasks.
- **User Authentication:** Secure registration and login using JWT.
- **Authorization:** Tasks are linked to users; a user can only manage their own tasks.
- **Pagination (Bonus):** Efficient retrieval of task lists.
- **Filtering (Bonus):** Filter tasks by `completed` status.

## 🛠️ Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repo_link>
    cd task-manager-api
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create the `.env` file:**
    Create a file named `.env` in the root directory and add your secret key:

    ```
    JWT_SECRET_KEY="your_secure_random_jwt_secret_key"
    ```

5.  **Initialize and run database migrations:**

    ```bash
    export FLASK_APP=app.py
    flask db init
    flask db migrate -m "Initial task and user models"
    flask db upgrade
    ```

6.  **Run the application:**
    ```bash
    flask run
    ```
    The API will be available at `http://127.0.0.1:5000/`.

## 📜 API Documentation and Examples

| Endpoint         | Method   | Description                                                    | Authentication |
| :--------------- | :------- | :------------------------------------------------------------- | :------------- |
| `/auth/register` | `POST`   | Create a new user account.                                     | No             |
| `/auth/login`    | `POST`   | Log in and receive an access token.                            | No             |
| `/tasks`         | `GET`    | Get a list of tasks (supports **pagination** & **filtering**). | Yes            |
| `/tasks`         | `POST`   | Create a new task.                                             | Yes            |
| `/tasks/<id>`    | `GET`    | Get details of a specific task.                                | Yes            |
| `/tasks/<id>`    | `PUT`    | Update a task.                                                 | Yes            |
| `/tasks/<id>`    | `DELETE` | Delete a task.                                                 | Yes            |

### Authentication Flow

#### 1. Register

**Request:**

```http
POST /auth/register
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}
```
