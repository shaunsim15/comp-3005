from flask import flash
from flask_wtf import FlaskForm
from fitness_club.models import Member, Trainer, Admin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    """This class represents the form for registering all users."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        '''To ensure that every email is unique in the database.'''
        Model = [Member, Admin, Trainer]
        for model in Model:
            user = model.query.filter_by(email=email.data).first()
            if user:
                flash('Email already exists, please choose another email.', 'danger')
                raise ValidationError('Email already exists, please choose another email.')
    

class MemberOnlyForm(RegistrationForm):
    """ Form for registering members only since it has additional fields."""
    goal_weight = StringField('Goal Weight', validators=[DataRequired()])
    goal_date = StringField('Goal Date', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])

class UpdateMemberForm(RegistrationForm):
    """ Form for updating member's information."""
    goal_weight = StringField('Goal Weight', validators=[DataRequired()])
    goal_date = StringField('Goal Date', validators=[DataRequired()])
    height = StringField('Height', validators=[DataRequired()])
    submit = SubmitField('Update')


class LoginForm(FlaskForm):
    """This class represents the form for logging in all users."""
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = StringField('Remember Me')
    submit = SubmitField('Login')
