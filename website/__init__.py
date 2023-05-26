from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "attendance.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Lecturer, Student, Level, Faculty, Department, Course

    # create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        app_ctx = app.app_context()
        app_ctx.push()
        db.create_all()
        app_ctx.pop()
        print('Created Database!')