import uuid

from flask import render_template, Blueprint, request, redirect, flash, url_for
from flask_login import login_required
# from sqlalchemy import in_

from app.models import Assign, Tickets, Trucks, Materials, Jobs, Customer
from app.forms import SearchForm, EditForm
from app import db

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
# @login_required
def index():

    form = SearchForm()
    page = request.args.get('page', 1, type=int)
    new_table = Assign.query.order_by(Assign.assignID.desc()).paginate(page=page, per_page=15)
    return render_template('index.html', new_table=new_table, form=form, Customer=Customer, Jobs=Jobs, Tickets=Tickets, Trucks=Trucks, Materials=Materials)

@main_blueprint.route('/intransit')
# @login_required
def intransit():

    page = request.args.get('page', 1, type=int)
    new_table = Assign.query.filter(Assign.Status == "InTransit").order_by(Assign.assignID.desc()).paginate(page=page, per_page=15)
    return render_template('intransit.html', new_table=new_table, Customer=Customer, Jobs=Jobs, Tickets=Tickets, Trucks=Trucks, Materials=Materials)



@main_blueprint.route('/search', methods=['POST'])
def search_controller():
    form = request.form
    print(22222222222222222)
    prepare = None
    if form['SubcontractorName']:
        prepare = Tickets.query.filter(Tickets.SubcontractorName == form['SubcontractorName'])
    if form['JobNumber'] and (prepare is None):
        prepare = Tickets.query.filter(Tickets.JobNumber == form['JobNumber'])
    elif form['JobNumber'] and prepare:
        prepare = prepare.filter(Tickets.JobNumber == form['JobNumber'])
    if form['MapscoLocation'] and (prepare is None):
        prepare = Tickets.query.filter(Tickets.JobNumber == form['MapscoLocation'])
    elif form['MapscoLocation'] and prepare:
        prepare = prepare.filter(Tickets.MapscoLocation == form['MapscoLocation'])
    if form['LoadOutNum'] and (prepare is None):
        prepare = Tickets.query.filter(Tickets.LoadOutNum == form['LoadOutNum'])
    elif form['LoadOutNum'] and prepare:
        prepare = prepare.filter(Tickets.LoadOutNum == form['LoadOutNum'])
    if form['TruckNumber']:
        trucks = Trucks.query.filter(Trucks.TruckNumber == ['TruckNumber']).all()
        truckids = [x.TruckID for x in trucks]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.TruckID.in_(truckids))
        else:
            prepare = prepare.filter(Tickets.TruckID.in_(truckids))
    if form['MaterialName']:
        materials = Materials.query.filter(Materials.MaterialName == form['MaterialName']).all()
        materialids = [x.MaterialID for x in materials]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.MaterialID.in_(materialids))
        else:
            prepare = prepare.filter(Tickets.MaterialID.in_(materialids))
    if form['JobName']:
        jobs = Jobs.query.filter(Jobs.JobName == form['JobName']).all()
        jobids = [x.JobID for x in jobs]
        if prepare is None:
            prepare = Tickets.query.filter(Tickets.JobID.in_(jobids))
        else:
            prepare = prepare.filter(Tickets.JobID.in_(jobids))
    if form['CustomerName']:
        customers = Customer.query.filter(Customer.CustomerName == form['CustomerName']).all()
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
        print(33333333333)
        print(ticket_id)
        print(333333333333)
        elem = Assign.query.filter(Assign.TicketID == ticket_id).first()
        if not elem:
            new = Assign(TicketID=ticket_id, Loads=form.loads.data, Status=form.status.data)
            assert new.Loads
            assert new.Status
            assert new.TicketID
            new.save()
        else:
            elem.Loads = form.loads.data
            elem.Status = form.status.data
            elem.save()
    else:
        flash('Wrong data', 'danger')
    return redirect(url_for("main.index"))

    # Assign.query.order_by(Assign.assignID.desc()).paginate(page=page, per_page=15)