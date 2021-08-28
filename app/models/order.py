import enum
from datetime import date
from sqlalchemy import Enum
from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Order(db.Model, ModelMixin):

    __tablename__ = 'torders'

    class City(enum.Enum):
        dal = "Dallas"
        fw = "Fort Worth"

    orderID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String(50))
    JobName = db.Column(db.String(100))
    MapscoLocation = db.Column(db.String(20))
    Source = db.Column(db.String(50))
    JobNumber = db.Column(db.String(20))
    MaterialName = db.Column(db.String(20))
    LoadTotal = db.Column(db.Integer)
    Status = db.Column(db.String(9))
    # Updates
    destination = db.Column(db.String(64))
    created = db.Column(db.Date, default=date.today())
    po = db.Column(db.String(64))
    city = db.Column(Enum(City))

    LoadDispatchTotal = db.Column(db.Integer)  # Required for backward compatibility

    dispatches = relationship('Dispatch')
