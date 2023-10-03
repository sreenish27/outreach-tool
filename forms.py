from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddContactForm(FlaskForm):
    name = StringField('Trainer Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Optional(), Email()])
    phone = StringField('Phone', validators=[Optional()])
    linkedin = URLField('LinkedIn', validators=[Optional()])
    twitter = URLField('Twitter', validators=[Optional()])
    website = URLField('Website', validators=[Optional()])
    speciality = StringField('Speciality/Niche', validators=[Optional()])
    experience = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0)])
    location = StringField('Location', validators=[Optional()])
    submit = SubmitField('Add')