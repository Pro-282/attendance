from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask

socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
app = Flask('website')