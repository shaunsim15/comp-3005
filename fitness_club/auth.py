# Code from https://github.com/pallets/flask/tree/3.0.2/examples/tutorial
# A middleground between corey schafer's directory approach, and to the routes.py+forms.py approach suggested by GPT and here: https://exploreflask.com/en/latest/organizing.html
from flask import Blueprint, render_template
from fitness_club import db, bcrypt
from fitness_club.models import Member, Trainer

users = Blueprint("auth", __name__, url_prefix="/auth")

@users.route("/register", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.index"))
    user_role = request.args.get("user_role")
    if user_role == "member":
        form = MemberOnlyForm()
    else:
        form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        if user_role == "member":
            user = Member(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
            password=hashed_password, goal_weight=form.goal_weight.data, goal_date=form.goal_date.data, height=form.height.data)
        elif user_role == "trainer":
            user = Trainer(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        else: 
            # user = Admin()
            return "invalid user role"
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.first_name.data}!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/sign_up.html", form=form, user_role=user_role)