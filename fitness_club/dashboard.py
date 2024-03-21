from flask import Blueprint, render_template

from fitness_club import db
from flask_login import login_required

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@dashboard.route("/index")
@login_required
def index():
    return render_template("dashboard.html")