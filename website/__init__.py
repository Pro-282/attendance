from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "attendance.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '5f2ac867f9c5aed0000edfd5'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    from .models import Lecturers, Students, Levels, Faculties, Departments, Courses

    create_database(app)

    return app

def create_database(app):

    if not path.exists('instance/' + DB_NAME):
        app_ctx = app.app_context()
        app_ctx.push()
        db.create_all()
        app_ctx.pop()
        print('Created Database!')


def populate_db(app):
    from .models import Lecturers, Students, Levels, Faculties, Departments, Courses

    app_ctx = app.app_context()
    app_ctx.push()
    
    level1 = Levels(level='100 level')
    level2 = Levels(level='200 level')
    level3 = Levels(level='300 level')
    level4 = Levels(level='400 level')
    level5 = Levels(level='500 level')

    engineering = Faculties(faculty='Faculty of Engineering')
    Agric = Faculties(faculty='Faculty of Agricultural Science')
    Science = Faculties(faculty='Faculty of Science')
    Arts = Faculties(faculty='Faculty of Arts')

    mechatronics = Departments(department='Mechatronics Engineering', faculty_id=1)
    computer = Departments(department='Computer Engineering', faculty_id=1)
    electrical = Departments(department='Electrical Electronics Engineering', faculty_id=1)
    physics = Departments(department='Physics', faculty_id=3)
    mathematics = Departments(department='Mathematics', faculty_id=3)
    fst = Departments(department='Food Science and Technology', faculty_id=2)
    cropScience = Departments(department='Crop Science', faculty_id=2)

    db.session.add(level1)
    db.session.add(level2)
    db.session.add(level3)
    db.session.add(level4)
    db.session.add(level5)
    db.session.add(engineering)
    db.session.add(Agric)
    db.session.add(Science)
    db.session.add(Arts)
    db.session.add(mechatronics)
    db.session.add(computer)
    db.session.add(electrical)
    db.session.add(physics)
    db.session.add(mathematics)
    db.session.add(fst)
    db.session.add(cropScience)
    db.session.commit()

    app_ctx.pop()
    print('Created Database!')