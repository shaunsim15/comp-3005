from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField
from wtforms.validators import DataRequired


class LogWeightForm(FlaskForm):
    weight = DecimalField('Weight', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])


class HeightForm(FlaskForm):
    height = DecimalField('Height', validators=[DataRequired()])
