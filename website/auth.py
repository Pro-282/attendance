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
                    password=form.password.data,
                    faculty_id=form.faculty.data,
                    department_id=department_id
                )
            # db.session.add(user_to_create)
            # db.session.commit()
            return redirect(url_for('views.home'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}', category='danger')
        
    return render_template('sign_up.html', form=form, user=current_user)