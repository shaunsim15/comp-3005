from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from fitness_club.models import Member
from sqlalchemy import or_
from fitness_club.auth_forms import UpdateMemberForm
from fitness_club import db

member = Blueprint("member", __name__)

@member.route("/member", methods=['GET', 'POST'])
@login_required
def members():
    """ A trainer can view all members. """

    if current_user.role != "Trainer":
        abort(404)

    search_term = ""
    if request.method == "POST":
        search_term = request.form.get("search_term")

    if search_term:
        members = Member.query.filter(or_(Member.email.ilike(f"%{search_term}%"),
            Member.first_name.ilike(f"%{search_term}%"),
            Member.last_name.ilike(f"%{search_term}%"))).all()
    else:
        members = Member.query.all()

    return render_template("member/index.html", members=members, search_term=search_term)


@member.route("/member/<int:member_id>", methods=['GET'])
@login_required
def member_show(member_id):
    """ A trainer can view a member's profile. """

    if current_user.role != "Trainer":
        abort(404)

    member = Member.query.get(member_id)
    if not member:
        flash("Member not found", "danger")
        return redirect(url_for("member.members"))

    return render_template("member/show.html", member=member)

@member.route("/member/profile/edit", methods=['GET', 'POST'])
@login_required
def update_member_profile():
    """ A member can update their profile. """
    if not hasattr(current_user, "goal_weight"):
        flash("You don't have access to edit", "danger")
        return redirect(url_for("home.index"))

    form = UpdateMemberForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.goal_weight = form.goal_weight.data
        current_user.goal_date = form.goal_date.data
        current_user.height = form.height.data
        db.session.add(current_user)
        db.session.commit()
        flash("Profile updated successfully", "success")
        return redirect(url_for("member.member_show", member=current_user))
    
    elif request.method == "GET":
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.goal_weight.data = current_user.goal_weight
        form.goal_date.data = current_user.goal_date
        form.height.data = current_user.height
    return render_template("member/edit.html", form=form)