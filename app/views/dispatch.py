from flask import render_template, Blueprint, session, redirect, flash, url_for, request
from flask_login import login_required

from app import db
from app.models import Order, Dispatch, Trucks
from app.forms import OrderForm, EditForm, DispatchForm

dispatch_blueprint = Blueprint("dispatch", __name__)


@dispatch_blueprint.route("/add_new_dispatch/<int:order_id>", methods=["POST"])
@login_required
def add_new_dispatch(order_id):
    form_dispatch = DispatchForm()
    order = Order.query.get(order_id)
    if form_dispatch.validate_on_submit():
        load_dispatched = form_dispatch.LoadsDispatched.data
        if form_dispatch.LoadsDispatched.data <= order.LoadTotal:
            if LoadsDispatchedTotal_function(order_id, load_dispatched) <= order.LoadTotal:
                Dispatch(
                    orderID=order_id,
                    TruckNumber=form_dispatch.TruckNumber.data,
                    LoadsDispatched=load_dispatched
                ).save()
                session['form_dispatch.value'] = ''
            else:
                session['form_dispatch.value'] = form_dispatch.TruckNumber.data
                flash(f"Total loads more than {order.LoadTotal}!", "danger")
                return redirect(url_for("dispatch.dispatch", order_id=order_id))
        else:
            session['form_dispatch.value'] = form_dispatch.TruckNumber.data
            flash(f"Loads need to be less or equal {order.LoadTotal}!", "danger")
    else:
        flash("Wrong data", "danger")
    return redirect(url_for("dispatch.dispatch", order_id=order_id))


@dispatch_blueprint.route("/delete_dispatch_index/<int:order_id>/<int:dispatch_id>", methods=["POST"])
@login_required
def delete_dispatch_index(order_id, dispatch_id):
    dispatch = Dispatch.query.filter(Dispatch.orderID == order_id).filter(Dispatch.dispatchID == dispatch_id).first()
    if dispatch:
        dispatch.delete()
    else:
        flash("Wrong data", "danger")
    return redirect(url_for("dispatch.dispatch", order_id=order_id))


@dispatch_blueprint.route("/dispatch.edit_dispatch_index/<int:order_id>/<int:dispatch_id>", methods=["POST"])
@login_required
def edit_dispatch_index(order_id, dispatch_id):
    if request.form:
        order = Order.query.get(order_id)
        dispatch = Dispatch.query.filter(Dispatch.orderID == order_id).filter(Dispatch.dispatchID == dispatch_id).first()
        if LoadsDispatchedTotal_function(order_id, int(request.form['LoadsDispatched']) - dispatch.LoadsDispatched) <= order.LoadTotal:
            dispatch.TruckNumber = request.form['TruckNumber']
            dispatch.LoadsDispatched = request.form['LoadsDispatched']
            dispatch.save()
        else:
            flash(f"Total loads more than {order.LoadTotal}!", "danger")
    else:
        flash("Wrong data", "danger")
    return redirect(url_for("dispatch.dispatch", order_id=order_id))


@dispatch_blueprint.route("/dispatch/<int:order_id>", methods=["GET"])
@login_required
def dispatch(order_id):
    form_edit = EditForm()
    form_dispatch = DispatchForm()
    truck_numbers = truck_nums()
    order_item = Order.query.get(order_id)
    form_dispatch.dispatches = Dispatch.query.filter(Dispatch.orderID == order_id).all()
    form_dispatch.value = session.get('form_dispatch.value', '')

    return render_template(
        "dispatch.html",
        order_item=order_item,
        form_edit=form_edit,
        form_dispatch=form_dispatch,
        truck_numbers=truck_numbers,
    )

def truck_nums():
    all_truck_numbers = db.session.query(Trucks.TruckNumber).distinct().order_by(Trucks.TruckNumber).all()
    return [j[0] for j in all_truck_numbers]

def LoadsDispatchedTotal_function(order_id, load_dispatched=0):
    if load_dispatched:
        dispatches = Dispatch.query.filter(Dispatch.orderID == order_id).all()
        return sum([i.LoadsDispatched for i in dispatches]) + load_dispatched
    else:
        dispatches = Dispatch.query.filter(Dispatch.orderID == order_id).all()
        return sum([i.LoadsDispatched for i in dispatches])
