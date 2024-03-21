import email_validator
from fitness_club import db, bcrypt, login_manager
from fitness_club.models import Member, Trainer, Admin
from flask_login import current_user, login_user, logout_user
from fitness_club.auth_forms import RegistrationForm, MemberOnlyForm, LoginForm
from flask import Blueprint, render_template, redirect, url_for, request, flash

users = Blueprint("auth", __name__, url_prefix="/auth")

@login_manager.user_loader
def load_user(user_id):
    """ This function is used to reload the user object from the user ID stored in the session. """
    for Model in [Member, Trainer, Admin]:
        user = Model.query.get(int(user_id))
        if user:
            return user


@users.route("/register", methods=("GET", "POST"))
def register():
    """ This function registers a new user. """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    user_role = request.args.get("user_role") # Get the type parameter from the url.
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
            user = Admin(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
            
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.first_name.data}!", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/sign_up.html", form=form, user_role=user_role)


@users.route("/login", methods=("GET", "POST"))
def login():
    """ This function logs in a user. """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    
    form = LoginForm()
    if form.validate_on_submit():

        user = None
        for Model in [Member, Trainer, Admin]:
            user = Model.query.filter_by(email=form.email.data).first()
            if user:
                break

        if user is None or not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Login unsuccessful. Please check email and password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)
        return redirect(url_for("dashboard.index"))
    return render_template("auth/login.html", form=form)


@users.route("/logout")
def logout():
    """ This function logs out a user. """
    logout_user()
    return redirect(url_for("auth.login"))