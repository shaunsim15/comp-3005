from flask import redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from fitness_club import db
from fitness_club.models import WeightLog, Member
from fitness_club.health_metrics_forms import LogWeightForm, HeightForm
from flask import Blueprint
from datetime import datetime

health_metrics = Blueprint("health_metrics", __name__)

@health_metrics.route("/", methods=["GET", "POST"])
@health_metrics.route("/index", methods=["GET", "POST"])
@login_required
def index():
    # Check if current user is a member
    if current_user.role != 'Member':
        flash("You are not authorized to see weight.", "danger")
        return redirect(url_for("home.index"))

    # Retrieve weight data for the current user
    weights = WeightLog.query.filter_by(member_id=current_user.member_id).all()

    # Extract dates and weights from the weight logs
    dates = [weight.date for weight in weights]
    weights_data = [weight.weight for weight in weights]

    # Retrieve goal weight and goal date for the current member
    member = Member.query.filter_by(member_id=current_user.member_id).first()
    goal_weight = member.goal_weight
    goal_date = member.goal_date

    log_weight_form = LogWeightForm()
    if log_weight_form.validate_on_submit():
        # Retrieve weight and date from the form
        weight = log_weight_form.weight.data
        date = log_weight_form.date.data

        # Check if the provided date is not greater than today's date
        if date > datetime.now().date():
            flash("Date cannot be greater than today's date.", "danger")

        elif weight <= 0:
            flash("Invalid input. Please enter a valid weight", "danger")

        else:
            # Check if a record with the same combination of member_id and date exists
            existing_weight_log = WeightLog.query.filter_by(member_id=member.member_id, date=date).first()
            if existing_weight_log:
                # If a record exists, update the weight
                existing_weight_log.weight = weight
                db.session.commit()
                flash("Weight updated successfully!", "success")
                
            else:
                # If no record exists, create a new record
                new_weight_log = WeightLog(weight=weight, date=date, member_id=member.member_id)
                db.session.add(new_weight_log)
                db.session.commit()
                flash("Weight logged successfully!", "success")
                
            return redirect(url_for("health_metrics.index"))

    height_form = HeightForm()
    if height_form.validate_on_submit():
        height = height_form.height.data

        if(height>0):
            member.height = height
            db.session.commit()
            flash("Height updated successfully!", "success")
            return redirect(url_for("health_metrics.index"))
        else:
            flash("Invalid input. Please enter a valid height.", "danger")
            return redirect(url_for("health_metrics.index"))

    return render_template("health_metrics.html", dates=dates, weights=weights_data, goal_weight=goal_weight, goal_date=goal_date,log_weight_form=log_weight_form, height_form=height_form)
