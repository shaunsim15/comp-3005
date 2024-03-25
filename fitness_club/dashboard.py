from fitness_club import db
from flask_login import login_required, current_user
from flask import Blueprint, render_template


dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@dashboard.route("/index")
@login_required
def index():
    """ This route renders the dashboard page. """
    return render_template("dashboard.html", logged_user=current_user)
