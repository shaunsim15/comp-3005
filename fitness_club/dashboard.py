from fitness_club import db
from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for
from fitness_club.models import Member
from fitness_club.dashboard_forms import GoalForm


dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
@dashboard.route("/index")
@login_required
def index():
    """ This route renders the dashboard page. """
    return render_template("dashboard.html", logged_user=current_user)


@dashboard.route("/member-goals", methods=['GET', 'POST'])
def goal_setting():
    goal_form = GoalForm()
    if goal_form.validate_on_submit():
        # Retrieve goal weight and goal date from the form
        goal_weight = goal_form.goal_weight.data
        goal_date = goal_form.goal_date.data
        print(goal_weight)
        print(goal_date)

        
        # Get the current logged-in member
        member = Member.query.filter_by(member_id = current_user.member_id).first()
        if member:
            print("Hi")
            # Update the member's goal weight and goal date
            member.goal_weight = goal_weight
            member.goal_date = goal_date
            db.session.commit()
            # Redirect to dashboard
            return redirect(url_for('dashboard.index'))

        
    return render_template("goal_setting.html", goal_form=goal_form)



    