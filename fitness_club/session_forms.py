from datetime import datetime
from flask import request
from flask_wtf import FlaskForm
from fitness_club.models import Member, Routine, Schedule, Session, Trainer, Admin
from wtforms import FieldList, FormField, SelectMultipleField, StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField, BooleanField, DecimalField, IntegerField, ValidationError
from wtforms.validators import DataRequired, NumberRange

# This is the FormField in the FieldList + FormField Combo https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields https://wtforms.readthedocs.io/en/2.3.x/fields/#field-enclosures
class RoutineCountForm(FlaskForm):
    routine_id = IntegerField('Routine ID')
    routine_name = StringField('Routine Name', validators=[DataRequired()])
    routine_count = IntegerField('Routine Count', default=None)

# This is the FormField in the FieldList + FormField Combo https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields https://wtforms.readthedocs.io/en/2.3.x/fields/#field-enclosures
class MemberPaidForm(FlaskForm):
    has_paid_for_choices = [(True, 'Yes'), (False, 'No')] # NOT A FORM FIELD!

    member_id = IntegerField('Member ID')
    member_name = StringField('Member Name', validators=[DataRequired()])
    has_paid_for = SelectField('Has Paid For', choices=has_paid_for_choices, default=False) # I used a SelectField instead of a Boolean field for nicer UX

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
    routines = FieldList(FormField(RoutineCountForm), label='Routines') # FieldList + FormField Combo needed because we have nested data within a form. SelectMultipleField is not good enough for the job.
    members = FieldList(FormField(MemberPaidForm), label='Participants (Members)') # FieldList + FormField Combo needed because we have nested data within a form. SelectMultipleField is not good enough for the job.

    submit = SubmitField('Create / Update') # This label would get shown on the submit button of both the NEW and EDIT views by default. To add different labels for 'Create' and 'Update', I used my own HTML elements and conditionals.

    def validate_start_time(self, start_time): # method automatically called during form validation as it follows the naming convention validate_<field_name>
        if (self.end_time.data - start_time.data).total_seconds() < 3600:
            raise ValidationError('The difference between start and end time must be at least 1 hour.')
        return True

    def validate_trainer_id(self, trainer_id):
        proposed_start = self.start_time.data
        proposed_end = self.end_time.data

        path_arguments = request.path.split('/')  # request.path = "/session/3/edit". Splitting gives: ['', 'session', '3', 'edit']

        # First, check the Trainer is available
        schedule = Schedule.query.filter(Schedule.trainer_id==trainer_id.data, Schedule.start_time <= proposed_start, Schedule.end_time >= proposed_end).first()

        # If Trainer doesnt have a free schedule, raise an error
        if schedule is None:
            raise ValidationError('The Trainer is not working during your proposed time.')
        
        # Find all Sessions involving the Trainer.
        sessions = Session.query.filter(Session.trainer_id == trainer_id.data).all()

        # Make sure none of them conflict with the proposed_start and proposed_end (unless they correspond to the Session being currently edited, for the EDIT route!)
        for sesh in sessions:
            # If this is being called on the EDIT route, and the id of the session we're trying to update (e.g. '3', from the URL) matches the id of the current session, that doesn't count as a conflict:
            if len(path_arguments) >= 2: # Check to avoid index OOB errors
                if path_arguments[-1] == 'edit' and path_arguments[-2] == str(sesh.session_id):
                    continue
            # If there is some kind of overlap between the proposed session and the currently existing session
            if (proposed_start <= sesh.start_time and proposed_end > sesh.start_time) or (sesh.start_time <= proposed_start and sesh.end_time > proposed_start):
                raise ValidationError('The Trainer is busy with another Session during your proposed time.')                
        
        # If all checks passed, great, create or update the Session
        return True

