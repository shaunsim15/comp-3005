from flask import redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from fitness_club import db
from fitness_club.models import Member
from fitness_club.goal_setting_forms import GoalForm
from datetime import datetime

from flask import Blueprint

goal_setting_bp = Blueprint("goal_setting_bp", __name__)

@goal_setting_bp.route("/member-goals", methods=['GET', 'POST'])
@login_required
def goal_setting():
    
    if current_user.role != 'Member':
        flash("You are not authorized to see that page", "danger")
        return redirect(url_for("home.index"))

    goal_form = GoalForm()
    if goal_form.validate_on_submit():

        goal_weight = goal_form.goal_weight.data
        goal_date = goal_form.goal_date.data
        member = Member.query.filter_by(member_id=current_user.member_id).first()

        if goal_date <= datetime.now().date():
            flash('Goal date must be in the future.', 'danger')
            return render_template("goal_setting.html", goal_form=goal_form)

        if goal_weight <= 0:
            flash('Goal weight must be greater than 0.', 'danger')
            return render_template("goal_setting.html", goal_form=goal_form)

        member.goal_weight = goal_weight
        member.goal_date = goal_date
        db.session.commit()
        return redirect(url_for("home.index"))

    return render_template("goal_setting.html", goal_form=goal_form)
