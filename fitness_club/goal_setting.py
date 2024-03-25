from flask import redirect, url_for, render_template, abort
from flask_login import login_required, current_user
from fitness_club import db
from fitness_club.models import Member
from fitness_club.goal_setting_forms import GoalForm

from flask import Blueprint

goal_setting_bp = Blueprint("goal_setting_bp", __name__)

@goal_setting_bp.route("/member-goals", methods=['GET', 'POST'])
@login_required
def goal_setting():
    
    if not isinstance(current_user, Member):
        abort(404)  # Return a 404 error if uesr is not a member
    goal_form = GoalForm()
    if goal_form.validate_on_submit():
        # Retrieve goal weight and goal date from the form
        goal_weight = goal_form.goal_weight.data
        goal_date = goal_form.goal_date.data

        # Get the current logged-in member
        member = Member.query.filter_by(member_id=current_user.member_id).first()
        if member:
            # Update the member's goal weight and goal date
            member.goal_weight = goal_weight
            member.goal_date = goal_date
            db.session.commit()
            # Redirect to dashboard
            return redirect(url_for('dashboard.index'))

    return render_template("goal_setting.html", goal_form=goal_form)
