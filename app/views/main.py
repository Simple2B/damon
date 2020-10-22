import uuid

from flask import render_template, Blueprint, request, redirect, flash, url_for, session
from flask_login import login_required


from app.models import Assign, Tickets, Trucks, Materials, Jobs, Customer
from app.forms import SearchForm, EditForm
from app import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
# @login_required
def index():

    form = SearchForm()
    form_edit = EditForm()
    page = request.args.get('page', 1, type=int)
    new_table = Assign.query.order_by(Assign.assignID.desc()).paginate(page=page, per_page=15)
    return render_template('index.html', new_table=new_table, form=form, form_edit=form_edit, Customer=Customer, Jobs=Jobs, Tickets=Tickets, Trucks=Trucks, Materials=Materials)

@main_blueprint.route('/intransit')
# @login_required
def intransit():

    page = request.args.get('page', 1, type=int)
    new_table = Assign.query.filter(Assign.Status == "InTransit").order_by(Assign.assignID.desc()).paginate(page=page, per_page=15)
    return render_template('intransit.html', new_table=new_table, Customer=Customer, Jobs=Jobs, Tickets=Tickets, Trucks=Trucks, Materials=Materials)



@main_blueprint.route('/search', methods=["GET", 'POST'])
def search_controller():
    if request.method == 'POST':
        form = SearchForm()
        session['formdata'] = request.form
    elif request.method == "GET":
        formdata = session.get('formdata', None)
        if formdata:
            form = SearchForm(
                CustomerName=formdata['CustomerName'],
                JobName=formdata['JobName'],
                MapscoLocation=formdata['MapscoLocation'],
                JobNumber=formdata['JobNumber'],
                MaterialName=formdata['MaterialName'],
                LoadOutNum=formdata['LoadOutNum'],
                TruckNumber=formdata['TruckNumber'],
                SubcontractorName=formdata['SubcontractorName']
                )
            form.validate()
    prepare = None
    if form.SubcontractorName.data:
        prepare = Tickets.query.filter(Tickets.SubcontractorName == form.SubcontractorName.data)
    if form.JobNumber.data and (prepare is None):
        prepare = Tickets.query.filter(Tickets.JobNumber == form.JobNumber.data)
    elif form.JobNumber.data and prepare:
        prepare = prepare.filter(Tickets.JobNumber == form.JobNumber.data)
    if form.MapscoLocation.data and (prepare is None):
        prepare = Tickets.query.filter(Tickets.JobNumber == form.MapscoLocation.data)
    elif form.MapscoLocation.data and prepare:
        prepare = prepare.filter(Tickets.MapscoLocation == form.MapscoLocation.data)
    if form.LoadOutNum.data and (prepare is None):
        prepare = Tickets.query.filter(Tickets.LoadOutNum == form.LoadOutNum.data)
    elif form.LoadOutNum.data and prepare:
        prepare = prepare.filter(Tickets.LoadOutNum == form.LoadOutNum.data)
    if form.TruckNumber.data:
        trucks = Trucks.query.filter(Trucks.TruckNumber == form.TruckNumber.data).all()
        truckids = [x.TruckID for x in trucks]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.TruckID.in_(truckids))
        else:
            prepare = prepare.filter(Tickets.TruckID.in_(truckids))
    if form.MaterialName.data:
        materials = Materials.query.filter(Materials.MaterialName == form.MaterialName.data).all()
        materialids = [x.MaterialID for x in materials]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.MaterialID.in_(materialids))
        else:
            prepare = prepare.filter(Tickets.MaterialID.in_(materialids))
    if form.JobName.data:
        jobs = Jobs.query.filter(Jobs.JobName == form.JobName.data).all()
        jobids = [x.JobID for x in jobs]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.JobID.in_(jobids))
        else:
            prepare = prepare.filter(Tickets.JobID.in_(jobids))
    if form.CustomerName.data:
        customers = Customer.query.filter(Customer.CustomerName == form.CustomerName.data).all()
        customerids = [x.CustomerID for x in customers]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.CustomerID.in_(customerids))
        else:
            prepare = prepare.filter(Tickets.CustomerID.in_(customerids))
    new_table = None
    page = request.args.get('page', 1, type=int)
    if prepare:
        new_table = prepare.order_by(Tickets.TicketID.desc()).paginate(page=page, per_page=15)
    form = EditForm()
    return render_template('search.html', new_table=new_table, form=form, Customer=Customer, Jobs=Jobs, Tickets=Tickets, Trucks=Trucks, Materials=Materials)

@main_blueprint.route('/add_record/<int:ticket_id>', methods=['POST'])
def add_record(ticket_id):
    form = EditForm()
    if form.validate_on_submit():
        elem = Assign.query.filter(Assign.TicketID == ticket_id).first()
        if not elem:
            new = Assign(TicketID=ticket_id, Loads=form.loads.data, Status=form.status.data)
            new.save()
        else:
            elem.Loads = form.loads.data
            elem.Status = form.status.data
            elem.save()
    else:
        flash('Wrong data', 'danger')
    return redirect(url_for("main.index"))

@main_blueprint.route('/edit_index/<int:assign_id>', methods=['POST'])
def edit_index(assign_id):
    form = EditForm()
    print(1111111111111)
    print(assign_id)
    print(1111111111111)
    if form.validate_on_submit():
        elem = Assign.query.get(assign_id)
        elem.Loads = form.loads.data
        elem.Status = form.status.data
        elem.save()
    else:
        flash('Wrong data', 'danger')
    return redirect(url_for("main.index"))
