from datetime import datetime, timedelta
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import MemberSession, Achievement, MemberAchievement, SessionRoutine, Session, Routine, WeightLog
from fitness_club import db

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/dashboard")
@login_required
def index():
    """ This route renders the dashboard page with recent achievements, sessions, routines, and average weight for all time. """
    # Retrieve personnel sessions done by the current user
    past_week_sessions = db.session.query(Session).join(MemberSession, Session.session_id == MemberSession.session_id).filter(MemberSession.member_id == current_user.member_id).filter(
        Session.is_group_booking == False).all()

    # Retrieve routines done by the current user
    past_week_routines = db.session.query(Routine, db.func.sum(SessionRoutine.routine_count)).join(SessionRoutine, Routine.routine_id == SessionRoutine.routine_id).join(
        Session, Session.session_id == SessionRoutine.session_id).join(MemberSession, Session.session_id == MemberSession.session_id).filter(
            MemberSession.member_id == current_user.member_id).group_by(Routine).all()

    # Retrieve the 5 most recent achievements
    recent_achievements = db.session.query(MemberAchievement, Achievement).join(Achievement, MemberAchievement.achievement_id == Achievement.achievement_id).filter(
        MemberAchievement.member_id == current_user.member_id).order_by(MemberAchievement.date.desc()).limit(5).all()

    # Calculate the average weight of the current user for all time
    average_weight_query = db.session.query(db.func.avg(WeightLog.weight)).filter(WeightLog.member_id == current_user.member_id)
    
    # For more info on the scalar function https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/
    average_weight = average_weight_query.scalar() 

    return render_template("dashboard.html", logged_user=current_user, past_week_sessions=past_week_sessions, past_week_routines=past_week_routines, recent_achievements=recent_achievements, average_weight=average_weight)

