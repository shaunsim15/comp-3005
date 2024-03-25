from flask import redirect, url_for, render_template, abort
from flask_login import login_required, current_user
from fitness_club import db
from fitness_club.models import Member, WeightLog
from fitness_club.dashboard_forms import LogWeightForm

from flask import Blueprint

health_metrics = Blueprint("health_metrics", __name__)

@health_metrics.route("/log-weight", methods=['GET', 'POST'])
@login_required
def log_weight():
    if not isinstance(current_user, Member):
        abort(404) 
    log_weight_form = LogWeightForm()
    if log_weight_form.validate_on_submit():
        # Retrieve weight and date from the form
        weight = log_weight_form.weight.data
        date = log_weight_form.date.data
        
        # Get the current logged-in member
        member = Member.query.get(current_user.member_id)
        if member:
            # Create a new WeightLog record
            weight_log = WeightLog(weight=weight, date=date, member_id=member.member_id)
            db.session.add(weight_log)
            db.session.commit()
            return redirect(url_for('dashboard.index'))  
        
    return render_template("health_metrics.html", log_weight_form=log_weight_form)
