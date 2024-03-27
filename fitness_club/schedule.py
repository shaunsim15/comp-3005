from flask import redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user
from flask import Blueprint
from fitness_club import db
from fitness_club.models import Schedule
from fitness_club.schedule_forms import ScheduleForm

schedule = Blueprint("schedule", __name__)

@schedule.route("/", methods=['GET'])
@schedule.route("/index", methods=['GET'])
@login_required
def schedule_index():
    """ This route renders the schedule page. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    schedules = Schedule.query.filter_by(trainer_id=current_user.trainer_id).all()
    return render_template("schedule/index.html", schedules=schedules)


@schedule.route("/new", methods=['GET', 'POST'])
@login_required
def new_schedule():
    """ This route renders the new schedule page. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    form = ScheduleForm()
    return render_template("schedule/new.html", form=form)

@schedule.route("/", methods=['POST', 'GET'])
@login_required
def create_schedule():
    """ This route creates a new schedule. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    form = ScheduleForm(request.form)
    if form.validate():
        schedule = Schedule(
            trainer_id=current_user.trainer_id,
            start_time=form.start_time.data,
            end_time=form.end_time.data
        )
        db.session.add(schedule)
        db.session.commit()
        flash("Schedule created successfully", "success")
    return redirect(url_for("schedule.schedule_index"))


@schedule.route("/<int:trainer_id>/edit", methods=['GET'])
@login_required
def edit_schedule(trainer_id):
    """ This route renders the edit schedule page. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    schedule = Schedule.query.get(trainer_id)
    if schedule.trainer_id != current_user.trainer_id:
        flash("Access denied", "danger")
        return redirect(url_for("schedule.schedule_index"))
    form = ScheduleForm(obj=schedule)
    return render_template("schedule/edit.html", form=form)


@schedule.route("/<int:trainer_id>/update", methods=['POST'])
@login_required
def update_schedule(trainer_id):
    """ This route updates a schedule. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    schedule = Schedule.query.get(trainer_id)
    if schedule.trainer_id != current_user.trainer_id:
        flash("Access denied", "danger")
        return redirect(url_for("schedule.schedule_index"))
    form = ScheduleForm(request.form)
    if form.validate():
        schedule.start_time = form.start_time.data
        schedule.end_time = form.end_time.data
        db.session.commit()
        flash("Schedule updated successfully", "success")
    return redirect(url_for("schedule.schedule_index"))

        




