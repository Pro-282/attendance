from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField, SubmitField
from wtforms.validators import length, EqualTo, DataRequired, Email, ValidationError
from website.models import Lecturers

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