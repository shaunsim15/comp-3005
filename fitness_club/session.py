from flask import Blueprint, render_template

from fitness_club import db
from fitness_club.models import Room

session = Blueprint('session', __name__) # This means "This file is a blueprint of our app, this file has links, URLs, defined here".

@session.route('/sessions', methods=['GET', 'POST']) # 1st arg: '/sessions' is the URL to get to the view.
def home():
    rooms = Room.query.all() # db.session.execute(db.select(Room).order_by(Room.room_id)).scalars()
    return render_template("session/index.html", rooms=rooms)
