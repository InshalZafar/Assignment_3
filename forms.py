from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, TextAreaField, IntegerField,
                     SubmitField, SelectField, DateField, FloatField,
                     HiddenField)
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class DestinationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location (City)', validators=[DataRequired()])
    country = StringField('Country', validators=[Optional()])
    category = SelectField('Category',
                           choices=[('Beach', 'Beach'), ('Mountain', 'Mountain'),
                                    ('City', 'City'), ('Adventure', 'Adventure'),
                                    ('Cultural', 'Cultural')])
    image_url = StringField('Cover Image URL')
    latitude = FloatField('Latitude', validators=[Optional()], default=0.0)
    longitude = FloatField('Longitude', validators=[Optional()], default=0.0)
    submit = SubmitField('Save Destination')


class ReviewForm(FlaskForm):
    content = TextAreaField('Review', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Post Review')


class ReplyForm(FlaskForm):
    content = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Reply')


class TravelPlanForm(FlaskForm):
    name = StringField('Plan Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    budget = FloatField('Budget (USD)', validators=[Optional()], default=0.0)
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save Plan')


class ProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)])
    avatar_color = StringField('Avatar Color', default='#d4af37')
    submit = SubmitField('Update Profile')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[Optional()])
    category = SelectField('Category',
                           choices=[('', 'All Categories'),
                                    ('Beach', 'Beach'), ('Mountain', 'Mountain'),
                                    ('City', 'City'), ('Adventure', 'Adventure'),
                                    ('Cultural', 'Cultural')],
                           validators=[Optional()])
    min_rating = IntegerField('Min Rating', validators=[Optional(), NumberRange(min=0, max=5)], default=0)
    submit = SubmitField('Search')
