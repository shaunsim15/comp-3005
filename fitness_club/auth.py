# Code from https://github.com/pallets/flask/tree/3.0.2/examples/tutorial
# A middleground between corey schafer's directory approach, and to the routes.py+forms.py approach suggested by GPT and here: https://exploreflask.com/en/latest/organizing.html
from flask import Blueprint, render_template
from fitness_club import db

users = Blueprint("auth", __name__, url_prefix="/auth")

@users.route("/register", methods=("GET", "POST"))
def register():
    return render_template("auth/sign_up.html")