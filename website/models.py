from . import db, bcrypt, login_manager
from flask_login import UserMixin
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

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Students(db.Model):
    matric_no = db.Column(db.String(15), primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

class Courses(db.Model):
    course_code = db.Column(db.String(10), primary_key=True)
    course_title = db.Column(db.String(150), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))
    staff_no = db.Column(db.String(20), db.ForeignKey('lecturers.id'))