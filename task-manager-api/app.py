# app.py

import os
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from config import Config
from models import db, bcrypt
from auth import auth_bp
from routes import tasks_bp

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Initialize JWTManager normally
    JWTManager(app)
    
    # Initialize migration
    Migrate(app, db)

    # ... (register blueprints)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # This will create the database and tables if they don't exist
        # For a robust setup, use `flask db upgrade` in the terminal (see instructions below)
        db.create_all() 
    app.run(debug=True)