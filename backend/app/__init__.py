from flask import Flask
from .config import Config
from .extensions import db, migrate, security
from .models import User, Role
from flask_security import SQLAlchemyUserDatastore

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    # Регистрируем роуты
    from .routes import main_blueprint
    app.register_blueprint(main_blueprint)

    return app
