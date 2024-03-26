from flask import redirect, url_for, render_template
from flask_login import login_required, current_user
from flask import Blueprint
from fitness_club import db

schedule = Blueprint("schedule", __name__)

@schedule.route("/", methods=['GET'])
@schedule.route("/index", methods=['GET'])
@login_required
def schedule_index():
    """ This route renders the schedule page. """
    return render_template("schedule/index.html", logged_user=current_user)
