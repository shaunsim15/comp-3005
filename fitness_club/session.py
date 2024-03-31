from flask import Blueprint, render_template, abort

from fitness_club import db
from fitness_club.models import Member, MemberSession, Room, Routine, Session, SessionRoutine, Trainer
from fitness_club.session_forms import MemberPaidForm, RoutineCountForm, SessionForm
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import or_, union

session = Blueprint('session', __name__) # 'session' is the name of the blueprint. __name__ represents the name of the current module. This variable is exported to __init__.py https://flask.palletsprojects.com/en/2.0.x/tutorial/views/

# INDEX ROUTE
@session.route('/', methods=['GET']) 
@session.route('/index', methods=['GET']) 
@login_required 
def sessions():
    if current_user.role == 'Member': 
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
def session_show(session_id):  # Get the session_id used in the GET request URL
    # Find the Session associated with the session_id
    session = Session.query.get_or_404(session_id)
    is_member = current_user.role == 'Member'

    # If logged in as Member
    if is_member: 
        # If the Session to be shown is not a Group session, and is not a Personal Session associated with the Member, don't show the page
        if (not session.is_group_booking) and (MemberSession.query.filter_by(member_id=current_user.member_id, session_id=session_id).first() == None):
            abort(404)

    # Find the Trainer associated with the session_id
    trainer = Trainer.query.get_or_404(session.trainer_id)
    trainer_name = trainer.first_name + " " + trainer.last_name

    # Get Routine data to show in the view
    sess = db.session 
    query_result = sess.query(Routine, SessionRoutine).join(SessionRoutine).filter(SessionRoutine.session_id == session_id)
    routines_data = [{'routine_id': routine.routine_id, 'routine_name': routine.name, 'routine_count': session_routine.routine_count} for routine, session_routine in query_result] # Mapping elements of the query_result array to get an array of objects 

    # Get Room data to show in the View
    room_capacity = Room.query.get(session.room_id).capacity if session.room_id is not None else None # Get room_capacity if a Room exists for this session, otherwise room_capacity = None
    
    # Get Member data to show in the View
    query_result = sess.query(Member, MemberSession).join(MemberSession).filter(MemberSession.session_id == session_id)
    members_data = [{'member_id': member.member_id, 'member_name': f'{member.first_name} {member.last_name}', 'has_paid_for': 'Yes' if member_session.has_paid_for else 'No'} for member, member_session in query_result]
    room_slots_filled = len(members_data)
    room_occupancy = f'{room_slots_filled}/{room_capacity}' if session.room_id else 'No room booked' # Reports the room occupancy e.g. 17/20
    if current_user.role == 'Member': # If current user is a member, we don't wanna show ANY members_data
        # Attempt to get current MemberSession, check if it exists
        query_result = sess.query(Member, MemberSession).join(MemberSession).filter(MemberSession.session_id == session_id, MemberSession.member_id == current_user.member_id).all()
        members_data = [{'member_id': member.member_id, 'member_name': f'{member.first_name} {member.last_name}', 'has_paid_for': 'Yes' if member_session.has_paid_for else 'No'} for member, member_session in query_result]

    form = SessionForm(routines=routines_data, members=members_data) # Populate the routines FieldList with initial data, and the members FieldList with initial data 
    routine_c_form = RoutineCountForm()
    member_p_form = MemberPaidForm()
    form.room_id.data = session.room_id
    form.room_id.choices = [(room.room_id, room.name) for room in Room.query.all()]
    form.room_id.choices.insert(0, (-1, 'None')) # Create a dummy room option with room_id = -1 and name = 'None'. Insert at index 0
    # Display the show view
    return render_template("session/show.html", session=session, form=form, trainer_name=trainer_name, routine_c_form=routine_c_form, member_p_form=member_p_form, room_occupancy=room_occupancy, is_member=is_member)

# NEW ROUTE
@session.route("/new", methods=['GET', 'POST'])
@login_required 
def session_new():
    """ This function creates a new Session. """

    # Define whether current_user is Member
    is_member = current_user.role == 'Member'

    # Get Routine data to show in the view
    query_result = Routine.query.all()
    routines_data = [{'routine_id': routine.routine_id, 'routine_name': routine.name, 'routine_count': 0} for routine in query_result] # Mapping elements of the query_result array to get an array of objects 
    
    query_result = Member.query.all()
    members_data = [{'member_id': member.member_id, 'member_name': f'{member.first_name} {member.last_name}', 'add_to_session': 'No'} for member in query_result]
    
    form = SessionForm(routines=routines_data, members=members_data)
    
    routine_c_form = RoutineCountForm()
    member_p_form = MemberPaidForm() 

    # Here, defining dropdown choices is necessary to show a dropdown for Trainers in the view, as opposed to forcing them to manually enter a trainer_id. Same for Rooms.
    form.trainer_id.choices = [(trainer.trainer_id, trainer.first_name + " " + trainer.last_name) for trainer in Trainer.query.all()]
    form.room_id.choices = [(room.room_id, room.name) for room in Room.query.all()]
    form.room_id.choices.insert(0, (-1, 'None')) # Create a dummy room option with room_id = -1 and name = 'None'. Insert at index 0
    
    # This code runs if form validation is successful
    if form.validate_on_submit():
        if is_member:
            # First, add a Session to the db
            sesh = Session(name=form.name.data, start_time=form.start_time.data, end_time=form.end_time.data, trainer_id=form.trainer_id.data, is_group_booking=False, pricing=20, room_id=None) # Create a Session using data from form. For security reasons, I am specifying separate values for is_group_booking, pricing & room_id even though they have default values in session_forms.py
            db.session.add(sesh)
            db.session.flush() # Flush to get primary keys, so sesh.session_id works

            # Second, add SessionRoutines to the db
            for routine in form.routines.data: # each routine looks like {'routine_id': 1, 'routine_name': 'Push Ups', 'routine_count': 1, 'csrf_token': 'ImMxNmQ2MGU3ZDM2YTI3M2I5MjBhN2VhN2Y5ZjZhZGJkMjJmZDBlNzIi.ZgHW-w.LmqbvzQt7c1R2Xzjnj2Aq1T-PCE'}
                if routine['routine_count'] > 0:
                    session_routine = SessionRoutine(session_id=sesh.session_id, routine_id=routine['routine_id'], routine_count=routine['routine_count'])
                    db.session.add(session_routine) # Fine to add directly, since this is NEW route, no conflicting existing records
            
            # Third, add MemberSessions to the db (only one, since Members can only create Personal sessions involving themselves)
            member_session = MemberSession(member_id=current_user.member_id, session_id=sesh.session_id, has_paid_for=False)
            db.session.add(member_session)
        else:
            # First, add a Session to the db
            room_id_to_add = None if form.room_id.data < 0 else form.room_id.data
            is_group_booking_to_add = form.is_group_booking.data == 'Yes'
            sesh = Session(name=form.name.data, start_time=form.start_time.data, end_time=form.end_time.data, trainer_id=form.trainer_id.data, is_group_booking=is_group_booking_to_add, pricing=form.pricing.data, room_id=room_id_to_add) # Create a Session using data from form. For security reasons, I am specifying separate values for is_group_booking, pricing & room_id even though they have default values in session_forms.py
            db.session.add(sesh)
            db.session.flush() # Flush to get primary keys, so sesh.session_id works

            # Second, add SessionRoutines to the db
            for routine in form.routines.data: # each routine looks like {'routine_id': 1, 'routine_name': 'Push Ups', 'routine_count': 1, 'csrf_token': 'ImMxNmQ2MGU3ZDM2YTI3M2I5MjBhN2VhN2Y5ZjZhZGJkMjJmZDBlNzIi.ZgHW-w.LmqbvzQt7c1R2Xzjnj2Aq1T-PCE'}
                if routine['routine_count'] > 0:
                    session_routine = SessionRoutine(session_id=sesh.session_id, routine_id=routine['routine_id'], routine_count=routine['routine_count'])
                    db.session.add(session_routine) # Fine to add directly, since this is NEW route, no conflicting existing records
            
            # Third, add MemberSessions to the db
            member_count = 0
            for member in form.members.data: # each member looks sth like {'member_id': 1, 'add_to_session': 'No'}
                if member['add_to_session'] == 'Yes': # If this member is supposed to be added to the session
                    # For personal bookings, this block checks that no more than 1 member can be added to the Session
                    if not is_group_booking_to_add:
                        member_count += 1
                        if member_count > 1:
                            db.session.rollback()
                            flash('Error: Cannot add more than one member to a Personal Session', 'danger')
                            db.session.close()
                            return redirect(url_for("session.sessions"))
                    
                    # Adds the member to the session
                    member_session = MemberSession(member_id=member['member_id'], session_id=sesh.session_id, has_paid_for=False)
                    db.session.add(member_session) # Fine to add directly, since this is NEW route, no conflicting existing records
        
        db.session.commit()
        flash(f"Session named {form.name.data} created!", "success")
        return redirect(url_for("session.sessions")) # Go to this page once Session creation succeeds
    
    # This flashes error messages that're rendered in base.html
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "danger")
    
    return render_template("session/new.html", form=form, routine_c_form=routine_c_form, member_p_form=member_p_form, is_member=is_member)

# EDIT ROUTE
@session.route("/<int:session_id>/edit", methods=['GET', 'POST'])
@login_required 
def session_edit(session_id):
    # Check that session exists!
    session = Session.query.get_or_404(session_id)

    # Define whether current_user is Member
    is_member = current_user.role == 'Member'

    # If logged in as Member
    if is_member: 
        # If the Session to be shown is not a Group session, and is not a Personal Session associated with the Member, don't show the page
        if (not session.is_group_booking) and (MemberSession.query.filter_by(member_id=current_user.member_id, session_id=session_id).first() == None):
            abort(404)

    # Get Routine data to show in the view
    query_result = Routine.query.all() 
    routines_data = [{'routine_id': routine.routine_id, 'routine_name': routine.name, 'routine_count': 0} for routine in query_result] # Mapping elements of the query_result array to get an array of objects 

    # Get Room data to show in the View
    room_capacity = Room.query.get(session.room_id).capacity if session.room_id is not None else None # Get room_capacity if a Room exists for this session, otherwise room_capacity = None

    members_data = None
    if is_member:
        # Show one entry, to allow the member to join or exit the session.
        members_data = [{'member_id': current_user.member_id, 'member_name': f'{current_user.first_name} {current_user.last_name}', 'add_to_session': 'No' } ]
    else:
        # Show all Members in the View
        query_result = Member.query.all()
        members_data = [{'member_id': member.member_id, 'member_name': f'{member.first_name} {member.last_name}', 'add_to_session': 'No' } for member in query_result]

    # Count how many slots currently filled 
    room_slots_filled = MemberSession.query.filter(MemberSession.session_id == session_id).count()
    room_occupancy = f'{room_slots_filled}/{room_capacity}' if session.room_id else 'No room booked' # Reports the room occupancy e.g. 17/20

    # Find the Trainer associated with the session_id
    trainer = Trainer.query.get_or_404(session.trainer_id)
    trainer_name = trainer.first_name + " " + trainer.last_name


    form = SessionForm(routines=routines_data, members=members_data) # Populate the routines FieldList with initial data, and the members FieldList with initial data 
    routine_c_form = RoutineCountForm() 
    member_p_form = MemberPaidForm()


    # Here, defining dropdown choices is necessary to show a dropdown for Trainers in the view, as opposed to forcing them to manually enter a trainer_id. Same for Rooms.
    form.is_group_booking.data = 'Yes' if session.is_group_booking else 'No'
    form.pricing.data = session.pricing
    form.trainer_id.choices = [(trainer.trainer_id, trainer.first_name + " " + trainer.last_name) for trainer in Trainer.query.all()]
    form.room_id.choices = [(room.room_id, room.name) for room in Room.query.all()]
    form.room_id.choices.insert(0, (-1, 'None')) # Create a dummy room option with room_id = -1 and name = 'None'. Insert at index 0
    if is_member:
        form.room_id.data = -1 if session.room_id is None else session.room_id

    
    # This code runs if form validation is successful
    if form.validate_on_submit():
        # First, update the Session in the db
        session.name=form.name.data
        session.start_time=form.start_time.data
        session.end_time=form.end_time.data 
        session.trainer_id=form.trainer_id.data
        room_id_to_add = None if form.room_id.data < 0 else form.room_id.data
        session.room_id = room_id_to_add

        # Second, add, update or delete SessionRoutines in the db
        for routine in form.routines.data: # each routine looks like {'routine_id': 1, 'routine_name': 'Push Ups', 'routine_count': 1, 'csrf_token': 'ImMxNmQ2MGU3ZDM2YTI3M2I5MjBhN2VhN2Y5ZjZhZGJkMjJmZDBlNzIi.ZgHW-w.LmqbvzQt7c1R2Xzjnj2Aq1T-PCE'}
            # If SessionRoutine already exists, we update or delete it:
            sesh_routine = SessionRoutine.query.filter_by(routine_id=routine['routine_id'], session_id=session_id).first()
            if sesh_routine:
                if routine['routine_count'] > 0: # Update
                    sesh_routine.routine_count = routine['routine_count']
                else: # Delete
                    db.session.delete(sesh_routine)
            else: # Else, If SessionRoutine doesnt exist, we add it or do nothing
                if routine['routine_count'] > 0: # Add
                    session_routine = SessionRoutine(session_id=session_id, routine_id=routine['routine_id'], routine_count=routine['routine_count'])
                    db.session.add(session_routine)

        # Third, add or remove or do nothing with each MemberSession from the db, based on 'add_to_session'. We never update MemberSessions, because can't change has_paid_for. I assume the form stops a Member from updating other Members' data!!
        for member in form.members.data: # each member looks sth like {'member_id': 1, 'add_to_session': 'No'}
            # If MemberSession already exists, we delete it or do nothing:
            member_sesh = MemberSession.query.filter_by(member_id=member['member_id'], session_id=session_id).first()
            if member_sesh:
                if member['add_to_session'] == 'No': # Delete, BUT MUST CHECK THEY HAVENT PAID YET!
                    if not member_sesh.has_paid_for:
                        db.session.delete(member_sesh)
                    else:
                        db.session.rollback()
                        flash('Error: Cannot remove a Member who has already paid for this Session', 'danger')
                        db.session.close()
                        return redirect(url_for("session.session_edit", session_id=session_id))    
            else: # Else, If MemberSession doesnt exist, we add it or do nothing
                if member['add_to_session'] == 'Yes': # Add
                    member_session = MemberSession(member_id=member['member_id'], session_id=session_id, has_paid_for=False) # A Member newly joining a Session must have has_paid_for = False!
                    db.session.add(member_session)                        
        # Commit results
        db.session.commit()
        flash(f"Session named {form.name.data} updated!", "success")
        return redirect(url_for("session.sessions")) # Go to this page once Session updating succeeds
    
    # This flashes error messages that're rendered in base.html
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "danger")
    
    return render_template("session/edit.html", form=form, session=session, trainer_name=trainer_name, routine_c_form=routine_c_form, member_p_form=member_p_form, is_member=is_member, room_occupancy=room_occupancy)

# DELETE ROUTE
@session.route("<int:session_id>/delete", methods=['POST'])
@login_required
def delete_session(session_id):
    # Check that session exists!
    session = Session.query.get_or_404(session_id)

    # Define whether current_user is Member
    is_member = current_user.role == 'Member'

    # If logged in as Member
    if is_member: 
        # If the Session to be shown is a Group session OR is not a Personal Session associated with the Member, don't allow deletion
        if (session.is_group_booking):
            flash('Error: Members cannot delete Group Sessions', 'danger')
            return redirect(url_for("session.session_show", session_id=session_id))
        elif MemberSession.query.filter_by(member_id=current_user.member_id, session_id=session_id).first() == None:
            flash('Error: Members cannot delete Personal Sessions that do not involve them', 'danger')
            return redirect(url_for("session.session_show", session_id=session_id))
    
    # Ensure no one has paid for the session yet
    member_sessions = MemberSession.query.filter_by(session_id=session_id).all()
    for mem_sesh in member_sessions:
        if mem_sesh.has_paid_for:
            flash('Error: Cannot delete a Session where at least one member has paid', 'danger')
            return redirect(url_for("session.session_show", session_id=session_id))      

    # Delete the Session. The cascade in the db should delete all MemberSessions and SessionRoutines
    db.session.delete(session)
    db.session.commit()
    flash('Your session has been deleted!', 'success')
    return redirect(url_for('session.sessions'))