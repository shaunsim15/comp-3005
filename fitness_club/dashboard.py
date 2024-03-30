from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import MemberSession, Achievement, MemberAchievement, SessionRoutine, Session, Routine
from fitness_club import db

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def index():
    """ This route renders the dashboard page with recent achievements, sessions, and routines done in the past week. """
    # This variable will be used to filter the data to show only the past week
    start_date = datetime.now() - timedelta(days=7)

    # Retrieve personnel sessions done by the current user in the past week
    past_week_sessions = db.session.query(Session).join(MemberSession, Session.session_id == MemberSession.session_id).filter(MemberSession.member_id == current_user.member_id).filter(
        Session.end_time >= start_date).filter(Session.end_time <= datetime.now()).filter(Session.is_group_booking == False).all()

    # Retrieve routines done by the current user in the past week
    past_week_routines = db.session.query(Routine, db.func.sum(SessionRoutine.routine_count)).join(SessionRoutine, Routine.routine_id == SessionRoutine.routine_id).join(
        Session, Session.session_id == SessionRoutine.session_id).join(MemberSession, Session.session_id == MemberSession.session_id).filter(
            MemberSession.member_id == current_user.member_id).filter(Session.end_time >= start_date).filter(Session.end_time <= datetime.now()).group_by(Routine).all()

    # Retrieve the 5 most recent achievements
    recent_achievements = db.session.query(MemberAchievement, Achievement).join(Achievement, MemberAchievement.achievement_id == Achievement.achievement_id).filter(
        MemberAchievement.member_id == current_user.member_id).order_by(MemberAchievement.date.desc()).limit(5).all()

    return render_template("dashboard.html", logged_user=current_user, past_week_sessions=past_week_sessions, past_week_routines=past_week_routines, recent_achievements=recent_achievements)
