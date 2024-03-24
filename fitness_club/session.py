from flask import Blueprint, render_template, abort

from fitness_club import db
from fitness_club.models import Room, Session, Trainer
from fitness_club.session_forms import SessionForm
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash

session = Blueprint('session', __name__) # 'session' is the name of the blueprint. __name__ represents the name of the current module. This variable is exported to __init__.py https://flask.palletsprojects.com/en/2.0.x/tutorial/views/

# INDEX ROUTE
@session.route('/', methods=['GET']) # '/' is a URL to get to the index view.
@session.route('/index', methods=['GET']) # '/index' is also a URL to get to the index view.
@login_required # This means a user must be logged in to use this view / route https://flask-login.readthedocs.io/en/latest/#login-example
def sessions():
    if current_user.role != 'Member': # 'Role' is a custom method we defined on each of the three models.
        return redirect(url_for("users.login")) # redirect generates a redirect response. url_for generates a URL for a given endpoint (specifically, the 'login' route in the 'users' blueprint)
        
    sessions = Session.query.all()
    # Display the index view
    return render_template("session/index.html", sessions=sessions) # Pass info to the view via the sessions variable.

# SHOW ROUTE
@session.route("/<int:session_id>", methods=['GET'])
@login_required 
def session_show(session_id):
    # Only show the session page if current user is a Member
    if current_user.role != 'Member': 
        return redirect(url_for("users.login")) 
        
    # Get the session_id used in the GET request URL. Find the associated Session & Trainer. Pass relevant info to the view
    form = SessionForm()
    session = Session.query.get_or_404(session_id) 
    trainer = Trainer.query.get_or_404(session.trainer_id)
    trainer_name = trainer.first_name + " " + trainer.last_name
    # Display the show view
    return render_template("session/show.html", session=session, form=form, trainer_name=trainer_name)

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



###################################################################
### List of Logic Checks (LC) TBD for Index: ###
# LC: If Member, only display: All Group Sessions and All Personal Sessions that have a MemberSession associated with the Member.
# LC: If Trainer/Admin, display: All Sessions

###################################################################
### List of Logic Checks (LC) TBD for Show: ###
# To-Dos (ANYBODY)
# LC: If ANYBODY, shud be able to SEE Routines (and their routine_count)
# LC: If ANYBODY, shud be able to SEE Room Capacity for a Session
# LC: If trainer/admin personal or trainer/admin group, shud be able to SEE Member Count, SEE individual Members (and ALL their has_paid_for) for a Group/Personal Session
# LC: If member, shud be able to SEE ONLY THEIR OWN has_paid_for for a Group/Personal Session

###################################################################
### List of FUnctionalities (FU), Logic Checks (LC) AND Database Updates (DU) TBD for New: ###

# To-Dos (ANYBODY) (can be part of reusable functions?)
# LC: If ANYBODY, shud check end-date-time > start-date-time 
# LC: If ANYBODY, shud check trainer is available in specified time
# FU: If ANYBODY, shud be able to CHOOSE routines (and their routine_count) for a Personal/Group Session (but ofc Member Group is impossible)
# LC: If ANYBODY (Optional) Shud check EACH Member for this Session not already enrolled in a session with the same time (no double booking of Members)
# DU: If ANYBODY, shud CREATE a Session (duh)
# DU: If ANYBODY, shud CREATE 0, 1 or multiple SessionRoutines if successful (must be done before MemberSession, else achievement/stats checking will be wrong).
# DU: If ANYBODY, shud CREATE 0 (Group/Personal), 1 (Group/Personal) or multiple MemberSessions (Group) if successful. For each MemberSession, has_paid_for should default to False since this is NEW route
# DU: If ANYBODY, If either of the 3 database updates above fails, DONT create ANY of them
# DU: If ANYBODY, each successful MemberSession creation should TRIGGER Updates to the MemberAchievement table. This logic is VERY complex if we deal with multiple achievements.

# To-Dos (Member Personal):
# If member personal, most logic already accounted for above

# To-Dos (Member Group):
# If member group, CANNOT BE CREATED!

# To-Dos (Trainer/Admin Personal):
# FU: If trainer/admin personal, in UI shud be able to CHOOSE ONLY ONE member for a Personal Session
# LC: If trainer/admin personal, must check that number of members is <=1 if is_group_booking=False. (ASIDE: If if is_group_booking=True, we can have number of members <= 1 or > 1, so no need to check this) 
# FU: If trainer/admin personal, shud be able to CHOOSE room (can be None or not None). 

# To-Dos (Trainer/Admin Group):
# FU: If trainer/admin group, in UI shud be able to CHOOSE memberSSS for a Group Session
# LC: If trainer/admin group, i.e. if is_group_booking=True, no checks on the number of members. 
# FU: If trainer/admin group, MUST PICK A room (cant be None). Why? If I don't pick a room to begin with, I have no way of knowing capacity, and no way of restricting further intake based on capacity. 

# To-Dos (MISC):
# LC: If member personal or trainer/admin personal (Optional), shud check there is at least 1 room with enough space before 'placing the booking with Null Room'. Doesnt fully solve problem because you might receive multiple bookings be reserved even if only 1 room available...
# LC: If trainer/admin personal or trainer/admin group, and we chose Non-None Room, must validate there are no other Sessions with start-end conflicting with start-end in this Room
# LC: If trainer/admin personal or trainer/admin group, and we chose Non-None Room, must validate this room has capacity to house as many Members as specified in the NEW form (trivial in the case of Personal, as just 1 Member). I assume room capacity is MEMBER capacity; I exclude the trainer's headcount
# FU: If trainer/admin personal or trainer/admin group, shud be able to CHOOSE pricing (to not 20). This shouldnt be modifiable afterwards (or else we might be 'cheating' custsomers). 


###################################################################
### List of FUnctionalities (FU), Logic Checks (LC) AND Database Updates (DU) TBD for Edit: ###

# To-Dos (ANYBODY) (can be part of reusable functions?)
# LC: If ANYBODY, shud check end-date-time > start-date-time 
# LC: If ANYBODY, shud check trainer is available in specified time
# FU: If ANYBODY, shud be able to CHOOSE routines (and their routine_count) for a Personal/Group Session (but ofc Member Group is impossible)
# FU: If ANYBODY, shud NOT be able to change pricing.
# LC: If ANYBODY (Optional) Shud check EACH Member for this Session not already enrolled in a session with the same time (no double booking of Members)
# DU: If ANYBODY, shud UPDATE a Session (If changes were made)
# DU: If ANYBODY, shud CREATE 0, 1 or multiple SessionRoutines if successful (must be done before MemberSession, else achievement/stats checking will be wrong).
# DU: If ANYBODY, shud CREATE 0 (Group/Personal), 1 (Group/Personal) or multiple MemberSessions (Group) if successful. For each MemberSession, has_paid_for should default to False since this is NEW route
# DU: If ANYBODY, If either of the 3 database updates above fails, DONT create ANY of them
# DU: If ANYBODY, each successful MemberSession creation should TRIGGER Updates to the MemberAchievement table. This logic is VERY complex if we deal with multiple achievements.

# To-Dos (Member Personal):
# FU: If member personal, 

# To-Dos (Member Group):
# FU: If member group, CANNOT EDIT session_id, Name, start/end time, is_group_booking, pricing, room_id, trainer_id, routines.
# FU: If member group, CAN ONLY ADD yourself as a SessionMember, or REMOVE yourself as a SessionMember (2 possible buttons).


# To-Dos (Trainer/Admin Personal):
# FU: If trainer/admin personal, in UI shud be able to CHOOSE ONLY ONE member for a Personal Session
# LC: If trainer/admin personal, must check that number of members is <=1 if is_group_booking=False. (ASIDE: If if is_group_booking=True, we can have number of members <= 1 or > 1, so no need to check this) 
# FU: If trainer/admin personal, shud be able to CHOOSE room (can be None or not None). 

# To-Dos (Trainer/Admin Group):
# FU: If trainer/admin group, in UI shud be able to CHOOSE memberSSS for a Group Session
# LC: If trainer/admin group, i.e. if is_group_booking=True, no checks on the number of members. 
# FU: If trainer/admin group, MUST PICK A room (cant be None). Why? If I don't pick a room to begin with, I have no way of knowing capacity, and no way of restricting further intake based on capacity. 

# To-Dos (MISC):
# LC: If member personal or trainer/admin personal (Optional), shud check there is at least 1 room with enough space before 'placing the booking with Null Room'. Doesnt fully solve problem because you might receive multiple bookings be reserved even if only 1 room available...
# LC: If trainer/admin personal or trainer/admin group, and we chose Non-None Room, must validate there are no other Sessions with start-end conflicting with start-end in this Room
# LC: If trainer/admin personal or trainer/admin group, and we chose Non-None Room, must validate this room has capacity to house as many Members as specified in the NEW form (trivial in the case of Personal, as just 1 Member). I assume room capacity is MEMBER capacity; I exclude the trainer's headcount
# FU: If trainer/admin personal or trainer/admin group, shud be able to CHOOSE pricing (to not 20). This shouldnt be modifiable afterwards (or else we might be 'cheating' custsomers). 


###################################################################


# List of Logic Checks TBD for Edit:
# If member, shud be able to CHOOSE routines for a Session
# Member should be able to UNREGISTER for group session without destroying it.
# If trainer/admin, shud be able to CHOOSE Members for a Session

# List of Logic Checks TBD for Delete:
# If member, can only delete All PERSONAL Sessions that have a MemberSession associated with the Member. Can't delete group sessions
# If member, deletion of Personal Session should delete the MemberSession and SessionRoutines


#############################################################################################
# BRAIN DUMP
# Variables: Index, Show, New, Edit or Delete?
# Variables: Member, Trainer, Admin or Logged Out? (Ignore Logged Out, alrd handled by @login_required)
# Variables: Group or Personal session?
# Variables: Is class full or not?
# Can't violate is_group_booking by booking multiple MemberSessions when it's false

# List of Logic Checks TBD for Members:
# 1) Add to MemberSession table whenever you make a Session with given Member
# 2) Ensure you can't view/edit/delete personal sessions that don't involve you
# 3) Ensure you can't delete group sessions that don't involve you
# 4) Whenever a MemberSession is added, add triggers that check Achievement milestones for Members.

# List of Logic Checks TBD for Trainer/Admin:

# List of Logic Checks TBD for Everyone:
# 1) Ensure you can't create a Session with start_time <= end_time
# 2) Ensure you can't create a Session if trainer unavailable
# 3) Ensure you can't create a Session if there's already a Session in that room at that time
# 4) Ensure you can't edit a Group Session to add more people than the room can hold.
# 5) Choose routines for the session
#############################################################################################
