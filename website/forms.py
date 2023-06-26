from flask_login import current_user, login_required
from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField, SubmitField, HiddenField
from wtforms.validators import length, EqualTo, DataRequired, Email, ValidationError
from .models import Lecturers, Levels, Courses


form = Blueprint('form', __name__)

class RegisterForm(FlaskForm):
    def validate_staff_no(self, staff_no_to_check):
        lecturer = Lecturers.query.filter_by(id=staff_no_to_check.data).first()
        if lecturer:
            raise ValidationError('Staff Number already exitst!')
    
    def validate_email_address(self, email_to_check):
        email_address = Lecturers.query.filter_by(email=email_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    staff_no = StringField(label='Staff Number', validators=[length(min=2, max=20), DataRequired()])
    first_name = StringField(label='First Name',validators=[length(min=1, max=150), DataRequired()])
    last_name = StringField(label='Last Name', validators=[length(min=1, max=150), DataRequired()])
    email_address = EmailField(label='Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm Password', validators=[length(min=8), EqualTo('password'), DataRequired()])
    faculty = SelectField(label='Faculty', id='faculty', validators=[DataRequired()], choices=[])
    department = SelectField(label='Department', id='department', validators=[DataRequired()], choices=[])
    submit = SubmitField(label='Create Account')

class loginForm(FlaskForm):
    staff_no = StringField(label='Staff Number', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class CourseForm(FlaskForm):
    course_code = StringField(label='Course Code', validators=[length(min=3, max=10), DataRequired()])
    course_title = StringField(label='Course Title', validators=[length(min=5, max=150), DataRequired()])
    level = SelectField(label='Level', id='level', validators=[DataRequired()])
    submit = SubmitField(label='Add Course')