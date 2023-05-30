from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)

@views.route('/lecturer', methods=['GET'])
def lecturer_home():
    return "<h2>A page to show login & signup for the lecturers <br>and some information about the usage of the system</h2>"