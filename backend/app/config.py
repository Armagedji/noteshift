import os
from flask import current_app
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///noteshift.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    RESULT_FOLDER = os.path.join(os.getcwd(), 'results')