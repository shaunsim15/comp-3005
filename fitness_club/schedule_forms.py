from flask_wtf import FlaskForm
from wtforms import SubmitField, DateTimeLocalField
from wtforms.validators import DataRequired

class ScheduleForm(FlaskForm):
    """ This class represents the schedule form. """
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField("Submit")