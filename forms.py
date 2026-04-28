from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class DestinationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    image_url = StringField('Image URL')
    submit = SubmitField('Save')

class ReviewForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

class TravelPlanForm(FlaskForm):
    name = StringField('Plan Name', validators=[DataRequired()])
    submit = SubmitField('Create Plan')