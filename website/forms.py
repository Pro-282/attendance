from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField, EmailField, SubmitField
from wtforms.validators import length, EqualTo, DataRequired, Email, email_validator

class RegisterForm(FlaskForm):
  staff_no = StringField(label='Staff Number', validators=[length(min=2, max=20), DataRequired()])
  first_name = StringField(label='First Name',validators=[length(min=1, max=150), DataRequired()])
  last_name = StringField(label='Last Name', validators=[length(min=1, max=150), DataRequired()])
  email_address = EmailField(label='Email Address', validators=[Email(), DataRequired()])
  password1 = PasswordField(label='Password', validators=[length(min=8), DataRequired()])
  password2 = PasswordField(label='Confirm Password', validators=[length(min=8), EqualTo('password1'), DataRequired()])
  faculty = SelectField(label='Faculty', id='faculty', validators=[DataRequired()], choices=[])
  department = SelectField(label='Department', id='department', validators=[DataRequired()], choices=[])
  submit = SubmitField(label='Create Account')