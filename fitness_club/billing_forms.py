from flask_wtf import FlaskForm
from fitness_club.models import Member, Routine, Trainer
from wtforms import FieldList, FormField, SelectMultipleField, StringField, PasswordField, SelectField, SubmitField, DateTimeLocalField, BooleanField, DecimalField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class BillingSubForm(FlaskForm): # This represents a Session that has not been paid for
    payment_choices = [('Yes', 'Yes'), ('No', 'No')] # NOT A FORM FIELD!

    session_id = IntegerField('Session ID')
    session_name = StringField('Session Name', validators=[DataRequired()])
    pricing = DecimalField('Session Cost (CAD)', validators=[DataRequired(), NumberRange(min=0)], default=20)
    payment_choice = SelectField('Do you want to pay for this Session?', choices=payment_choices, default=False) # I used a SelectField instead of a Boolean field for nicer UX

class BillingForm(FlaskForm):
    """This class represents the form for a Billing."""
    unpaid_sessions = FieldList(FormField(BillingSubForm), label='Unpaid Sessions') # FieldList + FormField Combo needed because we have nested data within a form. SelectMultipleField is not good enough for the job.

    submit = SubmitField('Pay') 
