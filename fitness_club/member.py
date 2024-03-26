from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from fitness_club.models import Member
from sqlalchemy import or_

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