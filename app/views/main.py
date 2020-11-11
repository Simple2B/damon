from flask import render_template, Blueprint, request, redirect, flash, url_for
from flask_login import login_required


from app import db
from app.models import Tickets, Materials, Jobs, Customer, Order, Dispatch, Trucks
from app.forms import OrderForm, EditForm, AssignForm


main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == 'GET':
        form_edit = EditForm()
        form_assign = AssignForm()
        truck_numbers = truck_nums()
        choices = [(number, number) for number in truck_numbers]
        choices.insert(0, ('', ''))
        form_assign.TruckNumberSelect.choices = choices
        page = request.args.get("page", 1, type=int)
        new_table = Order.query.order_by(Order.orderID.desc()).paginate(
            page=page, per_page=15
        )
        return render_template(
            "index.html",
            new_table=new_table,
            form_edit=form_edit,
            form_assign=form_assign,
            reversed=reversed,
            LoadsDispatched_function=LoadsDispatched_function,
        )


def LoadsDispatched_function(new_table_item):
    dispatches = Dispatch.query.filter(Dispatch.orderID == new_table_item.orderID).all()
    return sum([i.LoadsDispatched for i in dispatches])


@main_blueprint.route("/new_order", methods=["GET", "POST"])
@login_required
def new_order():
    if request.method == 'GET':
        job_numbers = job_nums()
        form = OrderForm()
        choices = [(number, number) for number in job_numbers]
        choices.insert(0, ('', ''))
        form.JobNumberSelect.choices = choices
        return render_template(
            "new_order.html",
            form=form,
        )
    elif request.method == 'POST':
        form = OrderForm()
        if form.lookup.data and (not form.submit.data):
            job_number_data = ''
            if form.JobNumberSelect.data != '':
                job_number_data = form.JobNumberSelect.data
            else:
                job_number_data = form.JobNumberString.data
            if job_number_data != '':
                job_numbers = job_nums()
                job_number = job_number_data
                # TODO: TAKE FIRST
                # prepare = Tickets.query.filter(Tickets.JobNumber == job_number).all()
                prepare = Tickets.query.filter(Tickets.JobNumber == job_number).first()

                if prepare:
                    form = OrderForm()
                    form.CustomerName.data = Customer.query.get(prepare.CustomerID).CustomerName
                    form.JobName.data = Jobs.query.get(prepare.JobID).JobName
                    form.MapscoLocation.data = prepare.MapscoLocation
                    form.JobNumberSelect.data = job_number
                    form.JobNumberString.data = job_number
                    form.MaterialName.data = Materials.query.get(prepare.MaterialID).MaterialName

                choices = [(number, number) for number in job_numbers]
                choices.insert(0, ('', ''))
                form.JobNumberSelect.choices = choices
            return render_template(
                "new_order.html",
                form=form,
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
    # prepare = Jobs.query.distinct(Jobs.JobNumber).order_by(Jobs.JobNumber).all()
    # res = []
    # for i in prepare:
    #     if Tickets.query.filter(Tickets.JobID == i.JobID).first():
    #         res.append(i)
    # return res
    all_job_numbers = db.session.query(Tickets.JobNumber).distinct().order_by(Tickets.JobNumber).all()
    return [j[0] for j in all_job_numbers]


def truck_nums():
    all_truck_numbers = db.session.query(Trucks.TruckNumber).distinct().order_by(Trucks.TruckNumber).all()
    return [j[0] for j in all_truck_numbers]


@main_blueprint.route("/add_assign/<int:order_id>", methods=["POST"])
@login_required
def add_assign(order_id):
    form = AssignForm()
    if form.validate_on_submit():
        truck_number = ''
        if form.TruckNumberSelect.data != '':
            truck_number = form.TruckNumberSelect.data
        else:
            truck_number = form.TruckNumberString.data
        new = Dispatch(
            orderID=order_id,
            TruckNumber=truck_number,
            LoadsDispatched=form.LoadsDispatched.data
        )
        new.save()
    else:
        flash("Wrong data", "danger")
    return redirect(url_for("main.index"))


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
# @main_blueprint.route("/search", methods=["GET", "POST"])
# @login_required
# def search_controller():
#     form = OrderForm()
#     if request.method == "POST":
#         session["formdata"] = request.form
#     elif request.method == "GET":
#         formdata = session.get("formdata", None)
#         if formdata:
#             form = OrderForm(
#                 CustomerName=formdata["CustomerName"],
#                 JobName=formdata["JobName"],
#                 MapscoLocation=formdata["MapscoLocation"],
#                 JobNumber=formdata["JobNumber"],
#                 MaterialName=formdata["MaterialName"],
#                 LoadOutNum=formdata["LoadOutNum"],
#                 TruckNumber=formdata["TruckNumber"],
#                 SubcontractorName=formdata["SubcontractorName"],
#             )
#             form.validate()
#     prepare = None
#     if form.SubcontractorName.data:
#         prepare = Tickets.query.filter(
#             Tickets.SubcontractorName == form.SubcontractorName.data
#         )
#     if form.JobNumber.data and (prepare is None):
#         prepare = Tickets.query.filter(Tickets.JobNumber == form.JobNumber.data)
#     elif form.JobNumber.data and prepare:
#         prepare = prepare.filter(Tickets.JobNumber == form.JobNumber.data)
#     if form.MapscoLocation.data and (prepare is None):
#         prepare = Tickets.query.filter(Tickets.JobNumber == form.MapscoLocation.data)
#     elif form.MapscoLocation.data and prepare:
#         prepare = prepare.filter(Tickets.MapscoLocation == form.MapscoLocation.data)
#     if form.LoadOutNum.data and (prepare is None):
#         prepare = Tickets.query.filter(Tickets.LoadOutNum == form.LoadOutNum.data)
#     elif form.LoadOutNum.data and prepare:
#         prepare = prepare.filter(Tickets.LoadOutNum == form.LoadOutNum.data)
#     if form.TruckNumber.data:
#         trucks = Trucks.query.filter(Trucks.TruckNumber == form.TruckNumber.data).all()
#         truckids = [x.TruckID for x in trucks]
#         if prepare is None:
#             prepare = Tickets.query.filter(Tickets.TruckID.in_(truckids))
#         else:
#             prepare = prepare.filter(Tickets.TruckID.in_(truckids))
#     if form.MaterialName.data:
#         materials = Materials.query.filter(
#             Materials.MaterialName == form.MaterialName.data
#         ).all()
#         materialids = [x.MaterialID for x in materials]
#         if prepare is None:
#             prepare = Tickets.query.filter(Tickets.MaterialID.in_(materialids))
#         else:
#             prepare = prepare.filter(Tickets.MaterialID.in_(materialids))
#     if form.JobName.data:
#         jobs = Jobs.query.filter(Jobs.JobName == form.JobName.data).all()
#         jobids = [x.JobID for x in jobs]
#         if prepare is None:
#             prepare = Tickets.query.filter(Tickets.JobID.in_(jobids))
#         else:
#             prepare = prepare.filter(Tickets.JobID.in_(jobids))
#     if form.CustomerName.data:
#         customers = Customer.query.filter(
#             Customer.CustomerName == form.CustomerName.data
#         ).all()
#         customerids = [x.CustomerID for x in customers]
#         if prepare is None:
#             prepare = Tickets.query.filter(Tickets.CustomerID.in_(customerids))
#         else:
#             prepare = prepare.filter(Tickets.CustomerID.in_(customerids))
#     new_table = None
#     page = request.args.get("page", 1, type=int)
#     if prepare:
#         new_table = prepare.order_by(Tickets.TicketID.desc()).paginate(
#             page=page, per_page=15
#         )
#     form = EditForm()
#     if not new_table:
#         return redirect(url_for("main.index"))
#     return render_template(
#         "search.html",
#         new_table=new_table,
#         form=form,
#         Customer=Customer,
#         Jobs=Jobs,
#         Tickets=Tickets,
#         Trucks=Trucks,
#         Materials=Materials,
#     )
