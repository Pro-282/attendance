from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory
from flask import make_response
from flask_login import login_required, current_user
from dependencies .dependent import db, create_record_table, CSV_FOLDER
from .forms import CourseForm, coursesToEnroll
from .models import Levels, Courses, Students, attendance_base, Enrolled_courses
from sqlalchemy import Column, not_, select, Table, Integer, String, text
from datetime import datetime
import os

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

@views.route('/take-attendance')
@login_required
def take_attendance():
    course_code = request.args.get('course')
    user=current_user
    course = Courses.query.filter_by(course_code=course_code).first()
    try:
        current_date = datetime.now().strftime('%d-%m-%Y')
        create_column_query = text(f"ALTER TABLE {course.course_code} ADD '{current_date}' VARCHAR(15) DEFAULT 'Absent'")
        with db.engine.connect() as connection:
            connection.execute(create_column_query)
    except Exception as e:
         if 'duplicate column name' in str(e):
             print(f"column already exists: {str(e)}")
         else:
             print(f"error: {str(e)}")
    return render_template('attendance.html', user=user, course=course)

@views.route('/get-records/<course_code>', methods=['GET'])
@login_required
def get_records(course_code):
    filename = f"csv_records/{course_code}_attendance.csv"
    full_path = os.path.join(CSV_FOLDER, filename)
    print(f"Trying to send file from: {full_path}")
    create_record_table(course_code, filename)

    return send_from_directory(os.path.abspath(CSV_FOLDER), f"{course_code}_attendance.csv", as_attachment=True, download_name=f"{course_code}_attendance.csv")

    # return send_from_directory(CSV_FOLDER, filename, as_attachment=True, download_name=filename)