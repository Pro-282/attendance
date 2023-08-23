from . import db, bcrypt, login_manager
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


@login_manager.user_loader
def load_User(user_id):
    return Lecturers.query.get(user_id)
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
    id = db.Column(db.String(20), primary_key=True) #Lecturers Staff Number is the id
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True)
    password_hash = db.Column(db.String(150))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    courses = db.relationship('Courses')

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correctness(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Students(UserMixin, db.Model):
    matric_no = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    finger_id = db.Column(db.Integer, unique=True)

    def check_first_name_correctness(self, submitted_name):
        return self.first_name == submitted_name
    
    def get_id(self):
           return (self.matric_no)
    
    enrolled_courses = db.relationship('Enrolled_courses')

class Courses(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    course_title = db.Column(db.String(150), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    staff_no = db.Column(db.String(20), db.ForeignKey('lecturers.id'))

    enrolled_courses = db.relationship('Enrolled_courses')

class Enrolled_courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(15), db.ForeignKey('students.matric_no'), nullable=False)
    course_code = db.Column(db.String(15), db.ForeignKey('courses.course_code'), nullable=False)

class attendance_base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    matric_no = db.Column(db.String(15), nullable=False)
    first_name = db.Column(db.String(150),nullable=False)