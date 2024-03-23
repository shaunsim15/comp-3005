from flask_wtf import FlaskForm
from fitness_club.models import Member, Trainer
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange
  
# I have been able to use a single SessionForm for both the NEW and EDIT routes, but you may need two separate ones for your purposes (and maybe more for Members, Admins, Trainers, etc)
class SessionForm(FlaskForm):
    group_booking_choices = [(True, 'Yes'), (False, 'No')] # NOT A FORM FIELD!

    """This class represents the form for creating / editing a Session."""
    name = StringField('Name', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    is_group_booking = SelectField('Group Booking', choices=group_booking_choices, default=False) # I used a SelectField instead of a Boolean field for nicer UX
    pricing = DecimalField('Pricing per person per hour (CAD)', validators=[DataRequired(), NumberRange(min=0)], default=20)
    room_id = IntegerField('Room', default=None)
    trainer_id = SelectField('Trainer', coerce=int) # I used a SelectField instead of a boolean for nicer UX

    submit = SubmitField('Create / Update') # This label would get shown on the submit button of both the NEW and EDIT views by default. To add different labels for 'Create' and 'Update', I used my own HTML elements and conditionals.