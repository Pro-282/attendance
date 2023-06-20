from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Lecturers, Departments, Faculties
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from website.forms import RegisterForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Lecturers.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='danger')
        else:
            flash('Email does not exist.', category='danger')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         staff_number = request.form.get('staffNo')
#         first_name = request.form.get('firstName')
#         last_name = request.form.get('LastName')    
#         email = request.form.get('email')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')
#         faculty = request.form.get('faculty')
#         department = request.form.get('department')

#         user = Lecturers.query.filter_by(staff_no=staff_number).first()
#         if user:
#             flash('User already exists.', category='danger')
#         elif Lecturers.query.filter_by(email=email).first():
#             flash('Email already exists', category='danger')
#         elif len(email) < 4:
#             flash('Email must be greater than 4 characters.', category='danger')
#         elif len(first_name) < 2:
#             flash('First name must be greater than 1 character.', category='danger')
#         elif password1 != password2:
#             flash('password dont match.', category='danger')
#         elif len(password1) < 7:
#             flash('password must be greater than 7 characters.', category='danger')
#         elif department == 0:
#             flash('select a department', category='danger')
#         else:
#             department_id = (Departments.query.filter_by(department=department).first()).id
#             print(f'department id chossen is: {department_id}')
#             new_user = Lecturers(
#                 staff_no=staff_number,
#                 first_name=first_name,
#                 last_name=last_name,
#                 email=email,
#                 password=generate_password_hash(password1, method='sha256'),
#                 faculty_id=faculty,
#                 department_id=department_id
#             )
#             # db.session.add(new_user)
#             # db.session.commit()
#             # login_user(user, remember=True)
#             flash('Account created!', category='success')
#             return redirect(url_for('views.home'))
            
#     return render_template("sign_up.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = RegisterForm()
    if request.method == 'POST':
        form.faculty.choices = [(faculty.id, faculty.faculty) 
                                for faculty in Faculties.query.all()]
        faculty_id = form.faculty.data
        form.department.choices = [(department.department, department.department) 
                                   for department in Departments.query.
                                   filter_by(faculty_id=faculty_id).all()]
        if form.validate_on_submit():
            department_id = (Departments.query.
                            filter_by(department=form.department.data).
                            first()).id
            user_to_create = Lecturers(
                    staff_no=form.staff_no.data,
                    first_name=form.first_name.data,
                    email=form.email_address.data,
                    password=form.password1.data,
                    faculty_id=form.faculty.data,
                    department_id=department_id
                )
            # db.session.add(user_to_create)
            # db.session.commit()
            return redirect(url_for('views.home'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                print(f'There was an error with creating a user: {err_msg}')
        
    return render_template('sign_up.html', form=form, user=current_user)