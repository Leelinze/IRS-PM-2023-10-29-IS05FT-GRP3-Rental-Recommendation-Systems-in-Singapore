from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class LoginForm(FlaskForm):
    
    username = StringField("Username")
    password = StringField("Password")
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField("username")
    password = StringField("password")
    confirmPassword = StringField("confirmPassword")
    submit = SubmitField('Sign Up')

