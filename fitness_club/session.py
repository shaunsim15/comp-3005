from flask import Blueprint, render_template, abort

from fitness_club import db
from fitness_club.models import Member, MemberSession, Room, Routine, Session, SessionRoutine, Trainer
from fitness_club.session_forms import RoutineCountForm, SessionForm
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import or_, union

session = Blueprint('session', __name__) # 'session' is the name of the blueprint. __name__ represents the name of the current module. This variable is exported to __init__.py https://flask.palletsprojects.com/en/2.0.x/tutorial/views/

# INDEX ROUTE
@session.route('/', methods=['GET']) # '/' is a URL to get to the index view.
@session.route('/index', methods=['GET']) # '/index' is also a URL to get to the index view.
@login_required # This means a user must be logged in to use this view / route https://flask-login.readthedocs.io/en/latest/#login-example
def sessions():
    print(current_user.member_id)
    if current_user.role == 'Member': # 'Role' is a custom method we defined on each of the three models.
        # https://stackoverflow.com/questions/7942547/using-or-in-sqlalchemy
        # https://www.slingacademy.com/article/left-outer-join-in-sqlalchemy/
        sessions = Session.query.outerjoin(Session.members).filter(
            or_(
                Session.members.any(member_id=current_user.member_id), 
                Session.is_group_booking == True
                )
            ).all()
    else:
        sessions = Session.query.all()
    
    # Display the index view
    return render_template("session/index.html", sessions=sessions) # Pass info to the view via the sessions variable.

# SHOW ROUTE
@session.route("/<int:session_id>", methods=['GET'])
@login_required 
def session_show(session_id):        
    # Get the session_id used in the GET request URL. Find the associated Session & Trainer. Pass relevant info to the view
    initial_data = [
        {'routine_id': 2, 'routine_name': 'pushups', 'routine_count': 3},
        {'routine_id': 4, 'routine_name': 'situps', 'routine_count': 5},
    ]
    form = SessionForm(routines=initial_data)
    routine_c_form = RoutineCountForm()
    session = Session.query.get_or_404(session_id)

    # If logged in as Member
    if current_user.role == 'Member': 
        # If the Session to be shown is not a Group session, and is not a Personal Session associated with the Member, don't show the page
        if (not session.is_group_booking) and (MemberSession.query.filter_by(member_id=current_user.member_id, session_id=session_id).first() == None):
            abort(404)

    routines = Routine.query.join(Routine.sessions).filter(
        Routine.sessions.any(session_id=session_id)
    ).all()

    print(routines)
    # form.populate_routines()

    trainer = Trainer.query.get_or_404(session.trainer_id)
    trainer_name = trainer.first_name + " " + trainer.last_name
    # Display the show view
    return render_template("session/show.html", session=session, form=form, trainer_name=trainer_name, routines=routines, routine_c_form=routine_c_form)

# NEW ROUTE
@session.route("/new", methods=['GET', 'POST'])
@login_required 
def session_new():
    """ This function creates a new Session. """
    # Only allow session creation if current user is a Member
    if current_user.role != 'Member': 
        return redirect(url_for("users.login")) 

    form = SessionForm()

    # Here, defining dropdown choices is necessary to show a dropdown for Trainers in the view, as opposed to forcing them to manually enter a trainer_id
    form.trainer_id.choices = [(trainer.trainer_id, trainer.first_name + " " + trainer.last_name) for trainer in Trainer.query.all()]

    # ASIDE: If we don't want a Member to be able to populate certain fields, we can delete them for Members, but not for Admins etc: https://wtforms.readthedocs.io/en/3.1.x/specific_problems/#removing-fields-per-instance
    
    # This code runs if form validation is successful
    if form.validate_on_submit():
        # Create a Session using data from form. For security reasons, I am specifying separate values for is_group_booking, pricing & room_id even though they have default values in session_forms.py
        session = Session(name=form.name.data, start_time=form.start_time.data, end_time=form.end_time.data, trainer_id=form.trainer_id.data, is_group_booking=False, pricing=20, room_id=None)
        db.session.add(session)
        db.session.commit()
        flash(f"Session named {form.name.data} created!", "success")
        return redirect(url_for("session.sessions")) # Go to this page once Session creation succeeds
    
    # This flashes error messages that're rendered in base.html
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "danger")

    # If form validation unsuccessful, go to this page (error messsages should be flashed too)
    return render_template("session/new.html", form=form)

# EDIT ROUTE
@session.route("/<int:session_id>/edit", methods=['GET', 'POST'])
@login_required 
def session_edit(session_id):
    # Only allow session editing if current user is a Member
    if current_user.role != 'Member': 
        return redirect(url_for("users.login")) 
    
    # To add: logic that prevents a member from editing a personal session that's not theirs

    # Check that session exists!
    session = Session.query.get_or_404(session_id) 

    form = SessionForm()

    # Here, defining dropdown choices is necessary to show a dropdown for Trainers in the view, as opposed to forcing them to manually enter a trainer_id
    form.trainer_id.choices = [(trainer.trainer_id, trainer.first_name + " " + trainer.last_name) for trainer in Trainer.query.all()]

    # This code runs if form validation is successful
    if form.validate_on_submit():
        # Update the relevant attributes of the existing Session record (not all need updating)
        session.name=form.name.data
        session.start_time=form.start_time.data 
        session.end_time=form.end_time.data 
        session.trainer_id=form.trainer_id.data
        db.session.commit()
        flash(f"Session named {form.name.data} updated!", "success")
        return redirect(url_for('session.session_show', session_id=session_id)) # Go to this page once Session updating succeeds
    
    # This flashes error messages that're rendered in base.html
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "danger")

    # If form validation unsuccessful, go to this page (error messsages should be flashed too)
    return render_template(f'session/edit.html', form=form, session=session)

# DELETE ROUTE
@session.route("<int:session_id>/delete", methods=['POST'])
@login_required
def delete_session(session_id):
    # Only allow Session deletion if current user is a Member
    if current_user.role != 'Member': 
        return redirect(url_for("users.login")) 
    
    # Check that session exists!
    session = Session.query.get_or_404(session_id)

    # To add: some way of checking this Member is authorized to delete this Session
    # if session.author != current_user:
    #     abort(403)

    # Delete the Session 
    db.session.delete(session)
    db.session.commit()
    flash('Your session has been deleted!', 'success')
    return redirect(url_for('session.sessions'))