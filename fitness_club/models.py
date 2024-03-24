# This is where you define the models of your application. https://exploreflask.com/en/latest/organizing.html
from . import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Member(db.Model, UserMixin): # Member inherits from 2 classes. db.Model is a SQL Alchemy class. SQL Alchemy is used for ORM; an instance of the Member class corresponds to a record in the db.
    """ This class represents the member model. """ # UserMixin is a class provided by Flask-Login (extension for managing user authentication). Inheriting from Flask-Login gives the Member class user-related functionality.
    __tablename__ = 'member' # This line sets the name of the database table associated with this model to 'member'

    member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    goal_weight = db.Column(db.Numeric(5, 2))
    goal_date= db.Column(db.Date)
    height = db.Column(db.Numeric(5, 2))

    def __repr__(self): # Provides a stringificaiton of the member object, kinda like toString() in Java
        return f"Member('{self.first_name}', '{self.last_name}', '{self.email}')"

    def get_id(self): # Gets the member_id in string form, just a method for instances of this class. Needed for the Flask-Login extension to work
        return str(self.member_id)

    @property # This decorator allows defining a method that can be accessed like an attribute. Role is a property of the Member class
    def role(self):
        return "Member"


class Trainer(db.Model, UserMixin):
    """ This class represents the trainer model. """
    __tablename__ = 'trainer'

    trainer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Trainer('{self.first_name}', '{self.last_name}', '{self.email}')"

    def get_id(self):
        return str(self.trainer_id)

    @property
    def role(self):
        return "Trainer"


class Admin(db.Model, UserMixin):
    """ This class represents the admin model. """
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def get_id(self):
        return str(self.admin_id)

    @property
    def role(self):
        return "Admin"


class Session(db.Model):
    __tablename__ = 'session'

    session_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    start_time = db.Column(db.TIMESTAMP)
    end_time = db.Column(db.TIMESTAMP)
    is_group_booking = db.Column(db.Boolean)
    pricing = db.Column(db.Numeric(8, 2), nullable=False) # maybe some constraint is needed here to reflect schema?
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


class WeightLog(db.Model):
    __tablename__ = 'weight_log'
    date = db.Column(db.Date, primary_key = True)
    weight = db.Column(db.Integer)
    member_id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return f"<WeightLog date={self.date} member_id={self.member_id}>"


    