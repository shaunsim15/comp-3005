from flask import redirect, url_for, render_template, request, flash
from flask_login import login_required, current_user
from flask import Blueprint
from fitness_club import db
from fitness_club.models import Schedule
from fitness_club.schedule_forms import ScheduleForm
from datetime import datetime

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


@schedule.route("/<start_time_str>", methods=['GET'])
@login_required
def show_schedule(start_time_str):
    """ This route shows a schedule. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    # start_time = datetime.strptime(start_time_str, "%Y-%m-%d%H%M")
    schedule = Schedule.query.filter_by(start_time=start_time_str).first()
    return render_template("schedule/show.html", schedule=schedule)


@schedule.route("/<start_time_str>/edit", methods=['GET'])
@login_required
def edit_schedule(start_time_str):
    """ This route renders the edit schedule page. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    schedule = Schedule.query.get((current_user.trainer_id, start_time_str))
    if schedule.trainer_id != current_user.trainer_id:
        flash("Access denied", "danger")
        return redirect(url_for("schedule.schedule_index"))
    form = ScheduleForm(obj=schedule)
    return render_template("schedule/edit.html", form=form, schedule=schedule)


@schedule.route("/<start_time_str>/update", methods=['POST', 'GET'])
@login_required
def update_schedule(start_time_str):
    """ This route updates a schedule. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    schedule = Schedule.query.get((current_user.trainer_id, start_time_str)) #query by composite primary key
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
    # return redirect(url_for("schedule.show_schedule", start_time_str=start_time_str))

        




