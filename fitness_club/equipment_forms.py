from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField
from wtforms.validators import DataRequired

class EquipmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_maintained_date = DateField('Last Maintained Date', validators=[DataRequired()])
    days_in_maintenance_interval = IntegerField('Days in Maintenance Interval', validators=[DataRequired()])
    room_id = IntegerField('Room ID', validators=[DataRequired()])
