from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .forms import CourseForm
from .models import Levels, Courses

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():    
    return render_template("home.html", user=current_user)

@views.route('/lecturer', methods=['GET', 'POST'])
@login_required
def lecturer_home():
    return render_template("lecturer.html", user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user=current_user
    courses = Courses.query.filter_by(staff_no=user.id).all()
    form = CourseForm()
    form.level.choices = [(level.id, level.level) for level in Levels.query.all()]
    if form.validate_on_submit():
        user = current_user
        course_to_add = Courses(
            course_code = form.course_code.data,
            course_title = form.course_title.data,
            faculty_id = user.faculty_id,
            department_id = user.department_id,
            level_id = form.level.data,
            staff_no = user.id
        )
        db.session.add(course_to_add)
        db.session.commit()
        flash(f'{course_to_add.course_title} was added successfully!', category='info')
        return redirect(url_for('views.dashboard'))
    return render_template("dashboard.html", user=current_user, form=form, courses=courses)

@views.route('/take-attendance-<course_code>')
@login_required
def take_attendance(course_code):
    print(course_code)
    return f'<h1>Attandance page for {course_code}</h1>'