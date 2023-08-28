from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from sqlalchemy import MetaData, Table, create_engine, text
import csv
import os
import sqlite3

socketio = SocketIO()
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
app = Flask('website')
DB_NAME = "attendance.db"
CSV_FOLDER = "csv_records"  # Folder where CSVs will be saved
os.makedirs(CSV_FOLDER, exist_ok=True)

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