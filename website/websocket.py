# from .models import Levels, Courses, Students, attendance_base, Enrolled_courses
from flask import Blueprint, request, current_app
from flask_socketio import emit, join_room
import threading
import time
from pyfingerprint.pyfingerprint import PyFingerprint
from website.models import Students, Enrolled_courses
from dependencies.dependent import db, socketio
# from dependencies.dependent import servo_init, play_tone, play_error, play_not_enrolled
from sqlalchemy import text
from datetime import datetime

websocket_bp = Blueprint('websocket', __name__)

# Flag to control the fingerprint loop
fingerprint_loop_running = False

# String to hold the course in Attendance 
attendanceCourseCode = "nil"

# Function to check fingerprints and emit results
def fingerprint_loop(app):
  global fingerprint_loop_running
  # pwm = servo_init() 
  try:
    with app.app_context():
      
      # Initialize fingerprint scanner
      try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
          raise ValueError('The given fingerprint sensor password is wrong!')
      except Exception as e:
        print('Error:', str(e))
        global fingerprint_loop
        fingerprint_loop_running = False
        return
          
      while fingerprint_loop_running:
        try:
          if f.readImage():
            f.convertImage(0x01)
            result = f.searchTemplate()
            if result[0] != -1:
              user_id = result[0]
              # Query your database to get user details based on user_id
              is_student = Students.query.filter_by(finger_id=user_id).first()
              if is_student:
                is_enrolled = Enrolled_courses.query.\
                              filter_by(matric_no = is_student.matric_no, 
                                        course_code = attendanceCourseCode)
                if is_enrolled:
                  current_date = datetime.now().strftime('%d-%m-%Y')
                  update_query = text(f"UPDATE {attendanceCourseCode} SET \
                                      '{current_date}' = 'Present' WHERE \
                                      matric_no = '{is_student.matric_no}' AND \
                                      first_name = '{is_student.first_name}';")
                  print(update_query)
                  with db.engine.connect() as connection:
                    connection.execute(update_query)
                    connection.commit()
                  # play_tone(500, 2) 
                  # Turn the servo to 90 degrees
                  # servo_init(90)
                  user_details = {
                    'name': f'{is_student.first_name}',
                    'matric_no': f'{is_student.matric_no}'
                  }
                  socketio.emit('attendance_result', user_details, 
                                namespace='/websocket', room=attendanceCourseCode)
                  # play_tone(880, 2)  # A5 for 1 second
                  # time.sleep(0.5)    # A brief pause
                  time.sleep(4)
                  # return the servo to 0 degrees
                  # play_tone(1500, 2)
                  # servo_init(0)
                else:
                  socketio.emit('attendance_result',
                                {'error': f'{is_student.matric_no} is not enrolled\
                                  for this Course'}, namespace='/websocket', 
                                  room=attendanceCourseCode)
                  # play_not_enrolled()
              else:
                # with app.app_context():  # Push a new application context
                socketio.emit('attendance_result', {'error': 'not a student'}, 
                              namespace='/websocket', room=attendanceCourseCode)
                # Replace the follfowing with your database query logic
                # play_error()
            else:
              # with app.app_context():  # Push a new application context
              socketio.emit('attendance_result', 
                            {'error': 'Fingerprint not recognized'}, 
                            namespace='/websocket', room=attendanceCourseCode)
              # play_error()
            time.sleep(2)  # Delay before scanning next fingerprint
          else:
            time.sleep(0.1)
        except KeyboardInterrupt:
          break
        except Exception as e:
          if str(e) == "The image contains too few feature points":
            print(f"The image contains too few feature points")
            # play_error()
      
      # fingerprint_loop_running = False
  except Exception as e:
    # Log the exception
    print(f"Error in fingerprint_loop: {e}")
  finally:
    fingerprint_loop_running = False

@socketio.on('connect', namespace='/websocket')
def on_connect():
  print("socket connection asked")
  courseCode = request.args.get('courseCode')
  if courseCode:
    global attendanceCourseCode
    attendanceCourseCode = courseCode
    join_room(attendanceCourseCode)
    print(f"attendance course code has changed to {attendanceCourseCode}")
    emit('server_message', {'message': f'Connected to WebSocket for {courseCode}'})

# WebSocket event to start the fingerprint loop
@socketio.on('start_attendance', namespace='/websocket')
def start_attendance():
  print("starting attendance")
  global fingerprint_loop_running
  if not fingerprint_loop_running:
    fingerprint_loop_running = True
    app = current_app._get_current_object()  # Get the actual app object
    # pass the app context to the thread, for the db operation
    threading.Thread(target=fingerprint_loop, args=(app,)).start() # pass the app context to the thread, for the db operation
    emit('attendance_status', {'status': f'started for {attendanceCourseCode}'},
         room=attendanceCourseCode)

# WebSocket event to stop the fingerprint loop
@socketio.on('stop_attendance', namespace='/websocket')
def stop_attendance():
  global fingerprint_loop_running
  fingerprint_loop_running = False
  emit('attendance_status', {'status': f'stopped for {attendanceCourseCode}'},
       room=attendanceCourseCode)