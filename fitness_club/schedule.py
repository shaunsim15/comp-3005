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

def is_overlapping(trainer_id, new_start_time, new_end_time, current_schedule=None):
    """ This function checks if a schedule overlaps with another schedule. """
    if new_start_time >= new_end_time:
        return True, 'End time must be after start time'
    
    # Get all existing schedules for the trainer except the current schedule
    existing_schedules = Schedule.query.filter(
        Schedule.trainer_id == trainer_id,
        Schedule.start_time != current_schedule if current_schedule else True
    ).all()

    #for each existing schedule, check if the new schedule overlaps or if already exists
    for schedule in existing_schedules:
        if schedule.start_time < new_end_time <= schedule.end_time or \
            schedule.start_time <= new_start_time < schedule.end_time:
            return True, 'The new schedule overlaps with an existing schedule'
    return False, None

@schedule.route("/", methods=['POST', 'GET'])
@login_required
def create_schedule():
    """ This route creates a new schedule. """
    if current_user.role != "Trainer":
        return redirect(url_for("home.index"))
    form = ScheduleForm(request.form)

    if form.validate():
        start_time = form.start_time.data
        end_time = form.end_time.data
        # Check if the schedule overlaps with another schedule
        overlapping, message = is_overlapping(current_user.trainer_id, start_time, end_time)
        if overlapping:
            flash(message, "danger")
            return redirect(url_for("schedule.new_schedule"))
        else:
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
        new_start_time = form.start_time.data
        new_end_time = form.end_time.data
        # Check if the schedule overlaps with another schedule
        overlapping, message = is_overlapping(current_user.trainer_id, new_start_time, new_end_time, current_schedule=start_time_str)
        if overlapping:
            flash(message, "danger")
            return redirect(url_for("schedule.edit_schedule", start_time_str=start_time_str))
        else:
            schedule.start_time = form.start_time.data
            schedule.end_time = form.end_time.data
            db.session.commit()
            flash("Schedule updated successfully", "success")
    return redirect(url_for("schedule.schedule_index"))
    # return redirect(url_for("schedule.show_schedule", start_time_str=start_time_str))

        




