from app import db
from app.models.utils import ModelMixin


class Order(db.Model, ModelMixin):

    __tablename__ = 'torders'

    orderID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String(50))
    JobName = db.Column(db.String(100))
    MapscoLocation = db.Column(db.String(20))
    Source = db.Column(db.String(50))
    JobNumber = db.Column(db.String(20))
    MaterialName = db.Column(db.String(20))
    LoadTotal = db.Column(db.Integer)
    # LoadDispatchTotal = db.Column(db.Integer)
    Status = db.Column(db.String(9))
