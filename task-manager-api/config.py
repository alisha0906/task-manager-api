# config.py

import os
from datetime import timedelta

# Get the base directory of the project
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Database Configuration
    # Using SQLite for simplicity in this example
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Configuration (Secret key is loaded from the .env file)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'default-super-secret-key-123')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Bcrypt configuration for password hashing
    BCRYPT_LOG_ROUNDS = 12