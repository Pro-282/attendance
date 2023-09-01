from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from sqlalchemy import MetaData, Table, create_engine, text
import csv
import os
# import RPi.GPIO as GPIO
import time

socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
app = Flask('website')
DB_NAME = "attendance.db"
CSV_FOLDER = "csv_records"  # Folder where CSVs will be saved
os.makedirs(CSV_FOLDER, exist_ok=True)

BUZZER_PIN = 18

def create_record_table(table_name, output_filename):
  rows = []
  headers = []

  with db.engine.connect() as connection:
    result = connection.execute(text(f"SELECT * FROM {table_name};"))

    # Fetch the column headers
    headers = result.keys()
    print(headers)
    for row in result:
      rows.append(row)
      print(row)
  
  # Write the data to CSV
  with open(output_filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(headers)
    for row in rows:
      csvwriter.writerow(row)

  print(f"Data from {table_name} has been written to {output_filename}")

  return os.path.join(CSV_FOLDER, output_filename)

# def servo_init(angle):
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setwarnings(False)
#   GPIO.setup(17, GPIO.OUT)

# # Set the GPIO pin to PWM and set the frequency to 50 Hz
#   pwm = GPIO.PWM(17, 50)
#   pwm.start(0)

#   duty = angle / 18 + 2
#   GPIO.output(17, True)
#   pwm.ChangeDutyCycle(duty)
#   time.sleep(1)
#   GPIO.output(17, False)
#   pwm.ChangeDutyCycle(0)

#   pwm.stop()
#   GPIO.cleanup()

# def play_tone(frequency, duration):
#   GPIO.setmode(GPIO.BCM)
#   GPIO.setwarnings(False)
#   GPIO.setup(BUZZER_PIN, GPIO.OUT)

#   pwm = GPIO.PWM(BUZZER_PIN, 1)
#   pwm.start(50) 

#   pwm.ChangeFrequency(frequency)
#   time.sleep(duration)
#   pwm.ChangeFrequency(1)  # "Turn off" sound after the duration

#   pwm.stop()
#   GPIO.cleanup()

# def play_error():
#   play_tone(1600, 0.25)
#   time.sleep(0.25)
#   play_tone(1600, 0.25)
#   time.sleep(0.25)
#   play_tone(1600, 0.25)

# def play_not_enrolled():
#   play_tone(1500, 0.5)
#   time.sleep(0.5)
#   play_tone(1500, 0.5)
#   time.sleep(0.5)