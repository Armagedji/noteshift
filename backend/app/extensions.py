from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore

security = Security()
user_datastore = None
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cors = CORS()
