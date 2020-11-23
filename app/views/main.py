from flask import render_template, Blueprint, request, session, redirect, flash, url_for
from flask_login import login_required


from app import db
from app.models import Tickets, Materials, Jobs, Customer, Order, Dispatch, Trucks
from app.forms import OrderForm, EditForm, DispatchForm


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'GET':
        form_edit = EditForm()
        form_assign = DispatchForm()
        truck_numbers = truck_nums()
        page = request.args.get("page", 1, type=int)
        new_table = Order.query.order_by(Order.orderID.desc()).paginate(
            page=page, per_page=15
        )

        session['form_dispatch.value'] = ''

        return render_template(
            "index.html",
            new_table=new_table,
            form_edit=form_edit,
            form_assign=form_assign,
            reversed=reversed,
            truck_numbers=truck_numbers,
            LoadsDispatched_function=LoadsDispatched_function,
        )


def LoadsDispatched_function(new_table_item):
    dispatches = Dispatch.query.filter(Dispatch.orderID == new_table_item.orderID).all()
    return sum([i.LoadsDispatched for i in dispatches])


@main_blueprint.route("/new_order", methods=["GET", "POST"])
@login_required
def new_order():
    job_numbers = job_nums()
    if request.method == 'GET':
        form = OrderForm()
        return render_template(
            "new_order.html",
            form=form,
            job_numbers=job_numbers,
        )
    elif request.method == 'POST':
        form = OrderForm()
        if form.lookup.data and (not form.submit.data):
            if form.JobNumber.data:
                job_number = form.JobNumber.data
                # TODO: TAKE FIRST
                # prepare = Tickets.query.filter(Tickets.JobNumber == job_number).all()
                prepare = Tickets.query.filter(Tickets.JobNumber == job_number).first()

                if prepare:
                    form = OrderForm()
                    form.CustomerName.data = Customer.query.get(prepare.CustomerID).CustomerName
                    form.JobName.data = Jobs.query.get(prepare.JobID).JobName
                    form.MapscoLocation.data = prepare.MapscoLocation
                    form.JobNumber.data = job_number
                    form.MaterialName.data = Materials.query.get(prepare.MaterialID).MaterialName

            return render_template(
                "new_order.html",
                form=form,
                job_numbers=job_numbers,
            )
        if form.submit.data:
            form.lookup.data = True
            if form.validate_on_submit:
                new = Order(
                    CustomerName=form.CustomerName.data,
                    JobName=form.JobName.data,
                    MapscoLocation=form.MapscoLocation.data,
                    Source=form.Source.data,
                    JobNumber=form.JobNumber.data,
                    MaterialName=form.MaterialName.data,
                    LoadTotal=form.LoadTotal.data,
                )
                new.save()
                return redirect(url_for("main.index"))
            else:
                flash("Wrong data", "danger")


def job_nums():
    all_job_numbers = db.session.query(Tickets.JobNumber).distinct().order_by(Tickets.JobNumber).all()
    return [j[0] for j in all_job_numbers]


def truck_nums():
    all_truck_numbers = db.session.query(Trucks.TruckNumber).distinct().order_by(Trucks.TruckNumber).all()
    return [j[0] for j in all_truck_numbers]


@main_blueprint.route("/edit_order/<int:order_id>", methods=["POST"])
@login_required
def edit_order(order_id):
    form = EditForm()
    if form.validate_on_submit():
        elem = Order.query.get(order_id)
        elem.CustomerName = form.CustomerName.data
        elem.JobName = form.JobName.data
        elem.MapscoLocation = form.MapscoLocation.data
        elem.Source = form.Source.data
        elem.JobNumber = form.JobNumber.data
        elem.MaterialName = form.MaterialName.data
        elem.LoadTotal = form.LoadTotal.data
        elem.LoadDispatchTotal = form.LoadDispatchTotal.data
        elem.Status = form.Status.data
        elem.save()
    else:
        flash("Wrong data", "danger")
    return redirect(url_for("main.index"))


@main_blueprint.route("/delete_index/<int:order_id>", methods=["POST", "GET"])
@login_required
def delete_index(order_id):
    elem = Order.query.get(order_id)
    if elem:
        dispatches = Dispatch.query.filter(Dispatch.orderID == order_id).all()
        if dispatches:
            for i in dispatches:
                i.delete()
        elem.delete()

    else:
        flash("Wrong data", "danger")
    return redirect(url_for("main.index"))


@main_blueprint.route("/intransit")
@login_required
def intransit():
    page = request.args.get("page", 1, type=int)
    new_table = (
        Order.query.filter(Order.Status == "InTransit")
        .order_by(Order.orderID.desc())
        .paginate(page=page, per_page=15)
    )
    return render_template(
        "intransit.html",
        new_table=new_table,
        reversed=reversed,
        LoadsDispatched_function=LoadsDispatched_function,
    )
