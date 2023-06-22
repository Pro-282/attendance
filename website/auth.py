from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Lecturers, Departments, Faculties
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from website.forms import RegisterForm, loginForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = loginForm()
    if form.validate_on_submit():
        attempted_user = Lecturers.query.filter_by(id=form.staff_no.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.first_name}', category='success')
            return redirect(url_for('views.lecturer_home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
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
                    id=form.staff_no.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    email=form.email_address.data,
                    password=form.password.data,
                    faculty_id=form.faculty.data,
                    department_id=department_id
                )
            db.session.add(user_to_create)
            db.session.commit()
            flash(f'Account successfully created, You are now logged in as: {user_to_create.first_name}', category='success')
            login_user(user_to_create)
            return redirect(url_for('views.lecturer_home'))
        if form.errors != {}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating an account: {err_msg}', category='danger')
        
    return render_template('sign_up.html', form=form, user=current_user)