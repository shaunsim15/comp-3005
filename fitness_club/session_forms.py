from datetime import datetime
from flask import request
from flask_wtf import FlaskForm
from sqlalchemy import or_
from fitness_club.models import Member, Room, Routine, Schedule, Session, Trainer, Admin
from wtforms import FieldList, FormField, SelectMultipleField, StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField, BooleanField, DecimalField, IntegerField, ValidationError
from wtforms.validators import DataRequired, NumberRange, Optional

# def validate_members(self, members): # Normal validate method didnt get called. This Custom validation method also doesnt get called. https://wtforms.readthedocs.io/en/3.1.x/validators/#custom-validators
#     # If group session, all is good, no need to validate
#     print("VALIDATE MEMBERS")
#     print(self.is_group_booking.data)
#     if self.is_group_booking.data == 'Yes':
#         return True

#     # If personal session, check that there's at most one member enrolled
#     member_count = 0
#     for member_paid_form in self.members.entries:
#         print(member_paid_form.add_to_session.data)
#         if member_paid_form.add_to_session.data == 'Yes':
#             member_count += 1
#             if member_count > 1:
#                 raise ValidationError('Cannot have more than 1 member for a Personal Session')
#     return True

# This is the FormField in the FieldList + FormField Combo https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields https://wtforms.readthedocs.io/en/2.3.x/fields/#field-enclosures
class RoutineCountForm(FlaskForm):
    routine_id = IntegerField('Routine ID')
    routine_name = StringField('Routine Name', validators=[DataRequired()])
    routine_count = IntegerField('Routine Count', default=None, validators=[Optional()])

    def validate_routine_count(self, routine_count): # method automatically called during form validation as it follows the naming convention validate_<field_name>
        if routine_count.data is not None and routine_count.data < 0: # This serves as an extra check, though in effect does nothing; even though the method is being called, routine_count.data is ALWAYS 0 for any negative num due to some Form weirdness.
            raise ValidationError('Routine Count must be a non-negative integer')
        return True

# This is the FormField in the FieldList + FormField Combo https://stackoverflow.com/questions/30121763/how-to-use-a-wtforms-fieldlist-of-formfields https://wtforms.readthedocs.io/en/2.3.x/fields/#field-enclosures
class MemberPaidForm(FlaskForm):
    has_paid_for_choices = [('Yes', 'Yes'), ('No', 'No')] # NOT A FORM FIELD!
    add_to_session_choices = [('Yes', 'Yes'), ('No', 'No')] # NOT A FORM FIELD!

    member_id = IntegerField('Member ID')
    member_name = StringField('Member Name', validators=[DataRequired()])
    has_paid_for = SelectField('Has Paid For', choices=has_paid_for_choices, default='No') # I used a SelectField instead of a Boolean field for nicer UX
    add_to_session = SelectField('Add to Session?', choices=add_to_session_choices, default='No') # I used a SelectField instead of a Boolean field for nicer UX

# I have been able to use a single SessionForm for both the NEW and EDIT routes, but you may need two separate ones for your purposes (and maybe more for Members, Admins, Trainers, etc)
class SessionForm(FlaskForm):
    group_booking_choices = [('Yes', 'Yes'), ('No', 'No')] # NOT A FORM FIELD!

    """This class represents the form for creating / editing a Session."""
    name = StringField('Name', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    is_group_booking = SelectField('Group Booking', choices=group_booking_choices, default='No') # I used a SelectField instead of a Boolean field for nicer UX
    pricing = DecimalField('Pricing per person per hour (CAD)', validators=[DataRequired(), NumberRange(min=0)], default=20)
    room_id = SelectField('Room', coerce=int, default=-1) # I used a SelectField instead of a boolean for nicer UX. The -1 default corresponds to None, and is hardcoded in the route controller functions
    trainer_id = SelectField('Trainer', coerce=int) # I used a SelectField instead of a boolean for nicer UX
    routines = FieldList(FormField(RoutineCountForm), label='Routines', min_entries=0, validators=[Optional()]) # FieldList + FormField Combo needed because we have nested data within a form. SelectMultipleField is not good enough for the job.
    members = FieldList(FormField(MemberPaidForm), label='Participants (Members)', min_entries=0, validators=[Optional()]) # FieldList + FormField Combo needed because we have nested data within a form. SelectMultipleField is not good enough for the job.
    # Use of Optional- https://prettyprinted.com/tutorials/how-to-use-fieldlist-in-flask-wtf/

    submit = SubmitField('Create / Update') # This label would get shown on the submit button of both the NEW and EDIT views by default. To add different labels for 'Create' and 'Update', I used my own HTML elements and conditionals.

    def validate_start_time(self, start_time): # method automatically called during form validation as it follows the naming convention validate_<field_name>
        print("VALIDATE STARTIME")
        if (self.end_time.data - start_time.data).total_seconds() < 3600:
            raise ValidationError('The difference between start and end time must be at least 1 hour.')
        return True

    def validate_room_id(self, room_id):
        print("VALIDATE Room")

        # Check the current room (assuming we've booked a room) has enough space
        current_room = Room.query.filter(Room.room_id == self.room_id.data).first()
        if current_room is not None: # If we've booked a room
            member_count = 0
            for subform in self.members.entries:
                if subform.add_to_session.data == 'Yes':
                    member_count += 1
            if member_count > current_room.capacity:
                raise ValidationError(f'The Room capacity of {current_room.capacity} is less than the number of Members ({member_count}) that you wish to support.')

        # Check the current room hasnt already been booked during the proposed time
        proposed_start = self.start_time.data
        proposed_end = self.end_time.data

        path_arguments = request.path.split('/')  # request.path = "/session/3/edit". Splitting gives: ['', 'session', '3', 'edit']
        
        # Find all Sessions involving the Room, if there is one.
        sessions = Session.query.filter(Session.room_id == self.room_id.data).all()

        # Make sure none of them conflict with the proposed_start and proposed_end (unless they correspond to the Session being currently edited, for the EDIT route!)
        for sesh in sessions:
            # If this is being called on the EDIT route, and the id of the session we're trying to update (e.g. '3', from the URL) matches the id of the current session, that doesn't count as a conflict:
            if len(path_arguments) >= 2: # Check to avoid index OOB errors
                if path_arguments[-1] == 'edit' and path_arguments[-2] == str(sesh.session_id):
                    continue
            # If there is some kind of overlap between the proposed session and the currently existing session
            if (proposed_start <= sesh.start_time and proposed_end > sesh.start_time) or (sesh.start_time <= proposed_start and sesh.end_time > proposed_start):
                raise ValidationError('The Room has been booked for another Session during your proposed time.')    
    
    def validate_is_group_booking(self, is_group_booking): # method automatically called during form validation as it follows the naming convention validate_<field_name>
        print("VALIDATE GROUP")
        print(is_group_booking.data)
        print(self.room_id.data)
        if is_group_booking.data == 'Yes' and (self.room_id.data == -1):
            raise ValidationError('Must book a room for a group sesion.')

        # If personal session, check that there's at most one member enrolled
        member_count = 0
        for member_paid_form in self.members.entries:
            print(member_paid_form.add_to_session.data)
            if member_paid_form.add_to_session.data == 'Yes':
                member_count += 1
                if member_count > 1:
                    raise ValidationError('Cannot have more than 1 member for a Personal Session')       

        return True

    def validate_trainer_id(self, trainer_id):
        print("VALIDATE TRAINER")
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


