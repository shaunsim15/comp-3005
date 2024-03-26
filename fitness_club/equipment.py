from flask import Blueprint, render_template, abort
from flask import flash, redirect, render_template, url_for
from datetime import date, datetime
from fitness_club import db
from fitness_club.models import Equipment, Room
from fitness_club.equipment_forms import EquipmentForm 
from flask_login import current_user, login_required



equipment = Blueprint('equipment', __name__)

# INDEX ROUTE

@equipment.route("/", methods=["GET"])
@equipment.route("/index", methods=["GET"])
@login_required
def index():
    # Check if current user is an admin
    if current_user.role != 'Admin':  # Adjust authorization logic as needed
        flash("You are not authorized to see equipment.", "danger")
        return redirect(url_for("home.index"))
    
    # Retrieve equipment data
    equipments = Equipment.query.all()

    return render_template("equipment/index.html", equipments=equipments)



# Show Route
@equipment.route("/<int:equipment_id>", methods=['GET'])
@login_required 
def equipment_show(equipment_id):
    # Check if current user is an admin
    if current_user.role != 'Admin':  # Adjust authorization logic as needed
        flash("You are not authorized to see equipment.", "danger")
        return redirect(url_for("home.index"))
    
    # Find the equipment associated with the equipment_id and aborts with 404 if not found https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.get_or_404
    equipment = Equipment.query.get_or_404(equipment_id)

    return render_template("equipment/show.html", equipment=equipment)



# NEW ROUTE
@equipment.route("/new", methods=['GET', 'POST'])
@login_required
def equipment_new():
    # Check if current user is an admin
    if current_user.role != 'Admin':  # Adjust authorization logic as needed
        flash("You are not authorized to add new equipment.", "danger")
        return redirect(url_for("home.index"))
    
    form = EquipmentForm()

    if form.validate_on_submit():
        # Check if the room the user inputs exists
        room_id = form.room_id.data
        room = Room.query.get(room_id)
        if not room:
            flash("That room does not exist. Please choose a valid room.", "danger")
            return render_template("equipment/new.html", form=form)

        today = datetime.now().date()

        # Ensure last_maintained_date is not greater than today's date
        if form.last_maintained_date.data > today:
            flash("The Last maintained date field cannot be in the future.", "danger")
            return render_template("equipment/new.html", form=form)

        # Create a new equipment object using data from the form
        equipment = Equipment(
            name=form.name.data,
            last_maintained_date=form.last_maintained_date.data,
            days_in_maintenance_interval=form.days_in_maintenance_interval.data,
            room_id=room_id
        )
        
        try:
            # Add the equipment to the database session and commit the transaction
            db.session.add(equipment)
            db.session.commit()

            flash(f"Equipment named '{form.name.data}' created!", "success")
            return redirect(url_for("equipment.index"))
        except Exception as e:
            # Handle any database errors
            flash("An error occurred while creating the equipment. Please try again.", "danger")
            print("Error creating equipment:", e)

    return render_template("equipment/new.html", form=form)





# EDIT ROUTE

@equipment.route("/<int:equipment_id>/edit", methods=['GET', 'POST'])
@login_required 
def equipment_edit(equipment_id):

    # Check if current user is an admin
    if current_user.role != 'Admin':  # Adjust authorization logic as needed
        flash("You are not authorized to edit equipment.", "danger")
        return redirect(url_for("home.index"))
    
    equipment = Equipment.query.get_or_404(equipment_id)

    form = EquipmentForm()

    if form.validate_on_submit():
        
        if form.last_maintained_date.data > date.today():
            flash("Last maintained date cannot be set to a future date.", "danger")
            return render_template('equipment/edit.html', form=form, equipment=equipment)

        # Check if the last maintained date is not modified to a date earlier than the previous one
        if form.last_maintained_date.data < equipment.last_maintained_date:
            flash("Last maintained date cannot be set to a date earlier than the previous one.", "danger")
            return render_template('equipment/edit.html', form=form, equipment=equipment)


        room_id = form.room_id.data
        room = Room.query.get(room_id)
        if not room:
            flash("The specified room does not exist. Please choose a valid room.", "danger")
            return render_template("equipment/edit.html", form=form, equipment=equipment)

        
        equipment.name = form.name.data
        equipment.last_maintained_date = form.last_maintained_date.data
        equipment.days_in_maintenance_interval = form.days_in_maintenance_interval.data
        equipment.room_id = form.room_id.data

        db.session.commit()
        flash(f"Equipment named {form.name.data} updated!", "success")
        return redirect(url_for('equipment.index'))

    form.name.data = equipment.name
    form.last_maintained_date.data = equipment.last_maintained_date
    form.days_in_maintenance_interval.data = equipment.days_in_maintenance_interval
    form.room_id.data = equipment.room_id

    return render_template('equipment/edit.html', form=form, equipment=equipment)


# DELETE ROUTE
@equipment.route("/<int:equipment_id>/delete", methods=['POST'])
@login_required
def delete_equipment(equipment_id):
    if current_user.role != 'Admin':  # Adjust authorization logic as needed
        flash("You are not authorized to delete equipment.", "danger")
        return redirect(url_for("equipment.index"))
    
    # Check if the equipment exists
    equipment = Equipment.query.get_or_404(equipment_id)

    # Delete the equipment 
    db.session.delete(equipment)
    db.session.commit()
    flash('The equipment has been deleted!', 'success')
    return redirect(url_for('equipment.index'))
