# This is where you define the models of your application. https://exploreflask.com/en/latest/organizing.html
from . import db
from sqlalchemy.orm import relationship

class Member(db.Model):
    __tablename__ = 'member'

    member_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    goal_weight = db.Column(db.Numeric(5, 2))
    goal_date= db.Column(db.Date)
    height = db.Column(db.Numeric(5, 2))

class Trainer(db.Model):
    __tablename__ = 'trainer'

    trainer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Session(db.Model):
    __tablename__ = 'session'

    session_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    is_group_booking = db.Column(db.Boolean)
    pricing = db.Column(db.Numeric(8, 2), nullable=False) # maybe some constraint is needed here to reflect schema?
    is_room_confirmed = db.Column(db.Boolean)
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id', ondelete='SET NULL'))
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id', ondelete='SET NULL'))

    # relationship to Room & Trainer model
    room = db.relationship('Room', backref=db.backref('sessions', lazy=True))
    trainer = db.relationship('Trainer', backref=db.backref('sessions', lazy=True))

class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    capacity = db.Column(db.Integer)


# class Trainer(db.Model):
#     __tablename__ = 'trainer'

#     trainer_id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(20))
#     last_name = db.Column(db.String(20))
#     email = db.Column(db.String(50))
#     password = db.Column(db.String(255))