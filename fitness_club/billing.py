from flask import Blueprint, render_template, abort

from fitness_club import db
from fitness_club.billing_forms import BillingForm, BillingSubForm
from fitness_club.models import Member, MemberSession, Room, Routine, Session, SessionRoutine, Trainer
from fitness_club.session_forms import MemberPaidForm, RoutineCountForm, SessionForm
from flask_login import current_user, login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import or_, union
from sqlalchemy.orm import sessionmaker # https://www.geeksforgeeks.org/sqlalchemy-orm-creating-session/

billing = Blueprint('billing', __name__) # 'billing' is the name of the blueprint. __name__ represents the name of the current module. This variable is exported to __init__.py https://flask.palletsprojects.com/en/2.0.x/tutorial/views/

# INDEX ROUTE
@billing.route('/', methods=['GET']) # '/' is a URL to get to the index view.
@billing.route('/index', methods=['GET']) # '/index' is also a URL to get to the index view.
@login_required # This means a user must be logged in to use this view / route https://flask-login.readthedocs.io/en/latest/#login-example
def billings():
    if current_user.role == 'Trainer':
        return redirect(url_for("auth.login"))
    
    members = None
    if current_user.role == 'Member':
        members = Member.query.filter_by(member_id=current_user.member_id).all()
    else:
        members = Member.query.all()
    
    # Display the index view
    return render_template("billing/index.html", members=members) # Pass info to the view via the members variable.

# SHOW ROUTE
@billing.route("/<int:member_id>", methods=['GET'])
@login_required 
def billing_show(member_id):  # Get the member_id used in the GET request URL
    # Find the Member associated with the member_id
    member = Member.query.get_or_404(member_id)

    # If you're a Trainer, OR a Member who doesn't own this page
    if current_user.role == 'Trainer': 
        abort(404)
    elif current_user.role == 'Member': # Check first to prevent Index OOB
        if member_id != current_user.member_id:
            abort(404)

    is_member = current_user.role == 'Member'
    sess = db.session # https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/#query-the-data

    query_result = sess.query(Session, MemberSession).join(MemberSession).filter(MemberSession.member_id == member_id)
    session_data = [{'session_id': session.session_id, 'session_name': session.name, 'pricing': session.pricing, 'has_paid_for': member_session.has_paid_for} for session, member_session in query_result]

    unpaid_session_data = []
    paid_session_data = []
    for session in session_data:
        if session['has_paid_for']:
            paid_session_data.append(session)
        else:
            del session['has_paid_for']
            session['payment_choice'] = False
            unpaid_session_data.append(session)            
    
    form = BillingForm(unpaid_sessions=unpaid_session_data) # Populate the unpaid_sessions FieldList with initial data 
    billing_subform = BillingSubForm() # Initializes a form, similar to SessionForm. I'm only doing this to get the label, not super important
    # Display the show view
    return render_template("billing/show.html", member=member, form=form, billing_subform=billing_subform, paid_session_data=paid_session_data, is_member=is_member) # paid session data is for display only, not needed as a form


# EDIT ROUTE
@billing.route("/<int:member_id>/edit", methods=['GET', 'POST'])
@login_required 
def billing_edit(member_id):
    # Find the Member associated with the member_id
    member = Member.query.get_or_404(member_id)

    is_member = False
    # If you're a Trainer, OR a Member who doesn't own this page
    if current_user.role == 'Trainer': 
        abort(404)
    elif current_user.role == 'Member': # Check first to prevent Index OOB
        is_member = True
        if member_id != current_user.member_id:
            abort(404)
    
    sess = db.session

    query_result = sess.query(Session, MemberSession).join(MemberSession).filter(MemberSession.member_id == member_id)
    session_data = [{'session_id': session.session_id, 'session_name': session.name, 'pricing': session.pricing, 'has_paid_for': member_session.has_paid_for} for session, member_session in query_result]

    unpaid_session_data = []
    paid_session_data = []
    for session in session_data:
        if session['has_paid_for']:
            paid_session_data.append(session)
        else:
            del session['has_paid_for']
            session['payment_choice'] = 'No'
            unpaid_session_data.append(session)

    form = BillingForm(unpaid_sessions=unpaid_session_data) # Populate the unpaid_sessions FieldList with initial data 
    billing_subform = BillingSubForm() # Initializes a form, similar to SessionForm. I'm only doing this to get the label, not super important

    # This code runs if form validation is successful
    if form.validate_on_submit():
        # Update MemberSessions in the db (only the has_paid_for attribute, if it needs updating)
        for sesh in form.unpaid_sessions.data:
            if sesh['payment_choice'] == 'Yes':
                member_session =  MemberSession.query.filter_by(
                    member_id=member_id,
                    session_id=sesh['session_id'],
                    has_paid_for=False # Confirm has_paid_for is False, tho should alrd be.
                ).first()
                if member_session is None:
                    abort(404) 
                member_session.has_paid_for = True
        db.session.commit() # Commit to db

        flash(f"Sessions were paid for!", "success")
        return redirect(url_for('billing.billing_show', member_id=member_id)) # Go to this page once Session updating succeeds
    
    # This flashes error messages that're rendered in base.html
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in field '{getattr(form, field).label.text}': {error}", "danger")

    # If form validation unsuccessful, go to this page (error messsages should be flashed too)
    return render_template("billing/edit.html", member=member, form=form, billing_subform=billing_subform, paid_session_data=paid_session_data, is_member=is_member) # paid session data is for display only, not needed as a form