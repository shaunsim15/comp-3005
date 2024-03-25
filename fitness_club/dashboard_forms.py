from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class LogWeightForm(FlaskForm):
    weight = StringField('Weight', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
