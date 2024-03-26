from fitness_club import db
from flask_login import login_required, current_user
from flask import Blueprint, render_template


home = Blueprint("home", __name__)

@home.route("/")
@home.route("/index")
@login_required
def index():
    """ This route renders the user home/profile page. """
    return render_template("home.html", logged_user=current_user)