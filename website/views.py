from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from dependencies .dependent import db
from .forms import CourseForm, coursesToEnroll
from .models import Levels, Courses, Students, attendance_base, Enrolled_courses
from sqlalchemy import Column, not_, select, Table, Integer, String

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

        class New_course(attendance_base):
            __tablename__ = course_to_add.course_code
        db.create_all()
        
        flash(f'{course_to_add.course_title} was added successfully!',\
              category='info')
        return redirect(url_for('views.dashboard'))
    return render_template("dashboard.html", user=current_user, form=form,\
                           courses=courses)

@views.route('/student-dashboard', methods=['GET', 'POST'])
def student_dashboard():
    matric_no = request.args.get('matric_no')
    user=Students.query.get(matric_no)
    enrolled_courses = db.session.query(Enrolled_courses, Courses).\
                                        filter_by(matric_no=matric_no)
    enrolled_courses = enrolled_courses.join(Courses, Enrolled_courses.\
                                             course_code == Courses.course_code)
   
    subquery = select(Enrolled_courses.course_code).\
                        where(Enrolled_courses.matric_no == user.matric_no)
    to_enroll = db.session.query(Courses).filter(~Courses.course_code.in_(subquery))
    to_enroll = to_enroll.filter_by(department_id=user.department_id, 
                                    level_id=user.level_id)
    
    form = coursesToEnroll()
    form.courses.choices = [(course.course_code, f"{course.course_code}: \
                             {course.course_title}") for course in to_enroll.
                             all()]

    disable_submit = False
    if form.courses.choices == []:
        disable_submit = True
    
    if request.method == 'POST' and form.validate_on_submit():
        for data in form.courses.data:
            course_to_enroll = Enrolled_courses(matric_no=matric_no, 
                                                course_code=data)
            db.session.add(course_to_enroll)
            db.session.commit()
            
            table = Table(data, db.metadata, Column('matric_no', String), 
                          Column('first_name', String), autoload_with=db.engine,
                          extend_existing=True)
            # Insert data into the table
            db.session.execute(table.insert().values({"matric_no": user.matric_no,
                                                      "first_name": user.first_name}))
            db.session.commit()
        flash("Courses Added Successfully", category='info')
        return redirect(url_for('views.student_dashboard', matric_no=user.matric_no))
    
    return render_template("student_dashboard.html", user=user,\
                           enrolled=enrolled_courses, form=form, disabled=disable_submit)

@views.route('/take-attendance-<course_code>')
@login_required
def take_attendance(course_code):
    print(course_code)
    return f'<h1>Attandance page for {course_code}</h1>'

@views.route('/socket')
def index():
    return render_template('index.html')

