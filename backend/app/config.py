import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'some-random-salt'  # меняй на свою соль
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False  # отключить отправку email для упрощения
    SECURITY_POST_LOGIN_VIEW = '/'  # куда редиректить после логина
    SECURITY_POST_LOGOUT_VIEW = '/'  # куда после логаута
    SECURITY_POST_REGISTER_VIEW = '/'  # куда после регистрации
    SECURITY_UNAUTHORIZED_VIEW = '/login'  # куда при попытке зайти без логина
