from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange


class GoalForm(FlaskForm):
    goal_weight = StringField('Goal Weight', validators=[DataRequired()])
    goal_date = StringField('Goal Date', validators=[DataRequired()])


class LogWeightForm(FlaskForm):
    weight = StringField('Weight', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
