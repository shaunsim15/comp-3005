
from flask_wtf import FlaskForm
from wtforms import DecimalField, DateField
from wtforms.validators import DataRequired

class GoalForm(FlaskForm):
    goal_weight = DecimalField('Goal Weight', validators=[DataRequired()])
    goal_date = DateField('Goal Date', validators=[DataRequired()])
    