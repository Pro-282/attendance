from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Levels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(15), nullable=False, unique=True)

    students = db.relationship('Students')
    courses = db.relationship('Courses')

class Faculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(100), nullable=False)

    departments = db.relationship('Departments')
    lecturers = db.relationship('Lecturers')
    students = db.relationship('Students')
    courses = db.relationship('Courses')

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))

    lecturers = db.relationship('Lecturers')
    students = db.relationship('Students')
    courses = db.relationship('Courses')

class Lecturers(db.Model, UserMixin):
    staff_no = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    courses = db.relationship('Courses')

class Students(db.Model):
    matric_no = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

class Courses(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department = db.Column(db.Integer, db.ForeignKey('departments.id'))
    level = db.Column(db.Integer, db.ForeignKey('levels.id'))
    staff_no = db.Column(db.String(20), db.ForeignKey('lecturers.staff_no'))

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))