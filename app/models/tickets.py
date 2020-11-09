from app import db


class Tickets(db.Model):

    __tablename__ = 'tTickets'

    TicketID = db.Column(db.Integer, primary_key=True)
    SubcontractorName = db.Column(db.String(50))
    TruckID = db.Column(db.Integer)
    CustomerID = db.Column(db.Integer)
    JobID = db.Column(db.Integer)
    JobNumber = db.Column(db.String(20))
    MaterialID = db.Column(db.Integer)
    MapscoLocation = db.Column(db.String(20))
    LoadOutNum = db.Column(db.String(15))
