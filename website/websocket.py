# from .models import Levels, Courses, Students, attendance_base, Enrolled_courses
from flask import Blueprint
from flask_socketio import emit
import threading
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from website.models import Students, Enrolled_courses
from dependencies.dependent import db, socketio
from sqlalchemy import Table, select, Column, String
from datetime import datetime

websocket_bp = Blueprint('websocket', __name__)

# Flag to control the fingerprint loop
fingerprint_loop_running = False

# String to hold the course in Attendance 
attendanceCourseCode = "nil"

# Function to check fingerprints and emit results
def fingerprint_loop():
  global fingerprint_loop_running
  fingerprint_loop_running = True
  
  # Initialize fingerprint scanner
  try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
      raise ValueError('The given fingerprint sensor password is wrong!')
  except Exception as e:
    print('Error:', str(e))
    fingerprint_loop_running = False
    return
  
  while fingerprint_loop_running:
    try:
      if f.readImage():
        f.convertImage(0x01)
        result = f.searchTemplate()
        if result[0] == True:
          user_id = result[1]
          # Query your database to get user details based on user_id
          is_student = Students.query.filter_by(finger_id = user_id).first()
          if is_student:
            is_enrolled = Enrolled_courses.query.filter_by(matric_no = is_student.matric_no, course_code = attendanceCourseCode)
            if is_enrolled:
              current_date = datetime.now().strftime('%d-%m-%Y')
              table = Table(attendanceCourseCode, db.metadata, Column('matric_no', String), 
                          Column('first_name', String), autoload_with=db.engine,
                          extend_existing=True)
              update_stmt = {
                table.update().values()
              }
              update_query = f"update {attendanceCourseCode} set {current_date} = 'present' where matric_no = :matric_no"
              db.engine.execute(update_query)
              db.session.commit()

              # todo: mark the attendance list present
              # todo: open the servo
             
          # Replace the follfowing with your database query logic
          user_details = {
            'name': f'{is_student.first_name}',
            'matric_no': f'{is_student.matric_no}'
          }
          emit('attendance_result', user_details)
        else:
          emit('attendance_result', {'error': 'Fingerprint not recognized'})
        time.sleep(2)  # Delay before scanning next fingerprint
      else:
        time.sleep(0.1)
    except KeyboardInterrupt:
      break
  
  fingerprint_loop_running = False

@socketio.on('connect', namespace='/websocket<courseCode>')
def on_connect(courseCode):
  global attendanceCourseCode
  attendanceCourseCode = courseCode
  emit('server_message', {'message': 'Connected to WebSocket'})

@socketio.on('custom_event')
def handle_custom_event(data):
  emit('server_message', {'message': 'Received data: ' + data['data']})

# WebSocket event to start the fingerprint loop
@socketio.on('start_attendance')
def start_attendance():
  global fingerprint_loop_running
  if not fingerprint_loop_running:
    fingerprint_thread = threading.Thread(target=fingerprint_loop)
    fingerprint_thread.start()
    emit('attendance_status', {'status': f'started for {attendanceCourseCode}'})

# WebSocket event to stop the fingerprint loop
@socketio.on('stop_attendance')
def stop_attendance():
  global fingerprint_loop_running
  fingerprint_loop_running = False
  emit('attendance_status', {'status': f'stopped for {attendanceCourseCode}'})

#todo: create a new column for the date in when the start attendance button is clicked