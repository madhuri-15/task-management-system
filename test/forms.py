from test.models import User, Task
from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


## Define Registration form
class RegistrationForm(Form):

    fullname = StringField('Full Name', validators=[DataRequired(), Length(min=4, max=20)])
    role = StringField('Designation', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    admin = BooleanField('Signing up as a admin')
    submit = SubmitField('Sign Up')

    # Check if username or email already taken.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is taken. Please create another one!")
        
    def validate_username(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Account for this email already exists. Try login instead.")


## Define Login form
class LoginForm(Form):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')



## Define class for adding task
class TaskForm(Form):

    name = TextAreaField('Task description', validators=[DataRequired()])
    due_date = DateField('Due date', validators=[DataRequired()])
    status=StringField('Status')
    submit = SubmitField('Save')


## Define form class for updating task
class UpdateForm(Form):

    name = TextAreaField('Task description', validators=[DataRequired()])
    status=StringField('Status')
    submit = SubmitField('Save')