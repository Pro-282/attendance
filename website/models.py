from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# from sqlalchemy import Column, ForeignKey, Integer, Table

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String, unique=True, nullable=False)

    students = db.relationship('Student')
    courses = db.relationship('Course')

class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    faculty = db.Column(db.String(100), nullable=False)

    departments = db.relationship('Department')
    lecturers = db.relationship('Lecturer')
    students = db.relationship('Student')
    courses = db.relationship('Course')

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))

    lecturers = db.relationship('Lecturer')
    students = db.relationship('Student')
    courses = db.relationship('Course')

class Lecturer(db.Model, UserMixin):
    staff_no = db.Column(db.String(20), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    courses = db.relationship('Course')

class Student(db.Model):
    matric_no = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

class Course(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    department = db.Column(db.Integer, db.ForeignKey('department.id'))
    level = db.Column(db.Integer, db.ForeignKey('level.id'))
    staff_no = db.Column(db.String(20), db.ForeignKey('lecturer.staff_no'))

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))