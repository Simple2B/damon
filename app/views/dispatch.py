from flask import render_template, Blueprint, redirect, session, flash, url_for
from flask_login import login_required

from app import db
from app.models import Order, Dispatch, Trucks
from app.forms import OrderForm, EditForm, DispatchForm

dispatch_blueprint = Blueprint("dispatch", __name__)


@dispatch_blueprint.route("/add_new_dispatch/<int:order_id>", methods=["POST"])
@login_required
def add_new_dispatch(order_id):
    form_dispatch = DispatchForm()
    loads_dispatched = form_dispatch.LoadsDispatched.data
    session['add_new_dispatch'] = True
    
    return redirect(url_for("dispatch.dispatch", order_id=order_id))


@dispatch_blueprint.route("/delete_dispatch_index/<int:order_id>", methods=["POST", "GET"])
@login_required
def delete_dispatch_index(order_id):
    elem = Order.query.get(order_id)
    if elem:
        dispatches = Dispatch.query.filter(Dispatch.orderID == order_id).all()
        if dispatches:
            for i in dispatches:
                i.delete()
        elem.delete()

    else:
        flash("Wrong data", "danger")
    return redirect(url_for("dispatch.dispatch", order_id=order_id))


@dispatch_blueprint.route("/dispatch/<int:order_id>", methods=["GET"])
@login_required
def dispatch(order_id):
    if request.method == 'GET':
        form_edit = EditForm()
        form_dispatch = DispatchForm()
        form_dispatch.add_new_dispatch = session.get('add_new_dispatch', False)
        truck_numbers = truck_nums()
        order_item = Order.query.get(order_id)
    #     page = request.args.get("page", 1, type=int)
    #     new_table = Order.query.order_by(Order.orderID.desc()).paginate(
    #         page=page, per_page=15
    #     )
        return render_template(
            "dispatch.html",
            order_item=order_item,
            form_edit=form_edit,
            form_dispatch=form_dispatch,
            # reversed=reversed,
            truck_numbers=truck_numbers,
            # LoadsDispatched_function=LoadsDispatched_function,
        )

def truck_nums():
    all_truck_numbers = db.session.query(Trucks.TruckNumber).distinct().order_by(Trucks.TruckNumber).all()
    return [j[0] for j in all_truck_numbers]