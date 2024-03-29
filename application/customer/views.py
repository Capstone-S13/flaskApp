from . import CUSTOMER_BLUEPRINT
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_required, current_user
# from flask_security import login_required, current_user
import application.system as system

# Account Type
CUSTOMER = 0
STORE = 1

# Order Statuses
ORDER_SENT = "Order Sent"
ORDER_RECEIVED = "Order Received"
ROBOT_DISPATCHED = "Robot Dispatched"
WAITING_FOR_PARCEL = "Waiting for Parcel"
STORING_IN_STORE_HUB = "Storing in Store Hub"
AT_STORE_HUB = "At Store Hub"
BETWEEN_HUBS = "Between Hubs"
AT_DEST_HUB = "At Destination Hub"
DELIVERING_TO_DOORSTEP = "Delivering to Doorstep"
ARRIVED = "Arrived"
DELIVERED = "Delivered"
CANCELLED = "Cancelled"
FAILED = "Failed"

###############################
#### Customer Landing Page ####
###############################

@CUSTOMER_BLUEPRINT.route('/landing', methods=['GET'])
@login_required
def landing():
    stores = system.get_all_stores()
    storeNames, delivery, waypoints = system.get_customer_orders(current_user.id)
    # print(delivery)
    stores = [stores[0], stores[2], stores[1]]
    return render_template("customer/customerLanding.html",
                           customerId=current_user.id,
                           stores = stores,
                           storeNames=storeNames,
                           delivery=delivery,
                           waypoints = waypoints,
                           storeLinks = {
                                        'Grabbly': 'https://img.squadhelp.com/story_images/visual_images/1645022906-grabbly1.png?class=show',
                                        'Shoppee': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEsd5WmP1xg0StBYLO_NaoGG3Cw4JplQcwYw&usqp=CAU',
                                        'Vendor': 'https://i.imgur.com/ixqar30.jpg'
                                        })

# Customer Creating Order
@CUSTOMER_BLUEPRINT.route('/create/<string:storeId>')
@login_required
def create(storeId):
    error = system.create_order(current_user.id, storeId)
    if error:
        return "There was an error creating the order"
    else:
        flash("Order has been created")
        # flash("order successfully created", 'info')
        return redirect(url_for('customer.landing'))

# Changing Order Status
@CUSTOMER_BLUEPRINT.route('/order/<string:orderId>', methods=['POST'])
@login_required
def order(orderId):
    if request.method == "POST":
        new_status = request.form["order_button"]
        # print(new_status)
        error = system.set_order_status(current_user.id,
                                        orderId,
                                        new_status)
        if error:
            print("There was an error updating order status")
            print(error)
            return redirect(url_for('customer.landing'))
        if new_status == ORDER_RECEIVED:
            flash("Order received!")
        else:
            flash("Order updated!")

        return redirect(url_for('customer.landing'))

# Setting Waypoint for Collection
@CUSTOMER_BLUEPRINT.route('/order/waypoint/<string:orderId>', methods=['POST'])
@login_required
def set_waypoint(orderId):
    if request.method == "POST":
        new_waypoint = request.form["waypoint_selected"]
        system.set_new_waypoint(orderId, new_waypoint)
        flash(f"Waypoint updated to {new_waypoint}!")
        return redirect(url_for('customer.landing'))
    return redirect(url_for('customer.landing'))

################################
#### Customer Settings Page ####
################################

@CUSTOMER_BLUEPRINT.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        error = system.update_user(current_user.id,
                                    request.form["name"],
                                    request.form["email"],
                                    request.form["postalCode"],
                                    request.form["unit"])
        if error:
            print("error updating user details")
            return render_template("customer/customerSettings.html", user=current_user)
        flash("Details Updated")
        return redirect(url_for('customer.landing'))
    return render_template("customer/customerSettings.html", user=current_user)