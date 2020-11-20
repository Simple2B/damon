from app import db
from app.models.utils import ModelMixin
from sqlalchemy.orm import relationship


class Dispatch(db.Model, ModelMixin):

    __tablename__ = 'tDispatch'

    dispatchID = db.Column(db.Integer, primary_key=True)
    orderID = db.Column(db.Integer, db.ForeignKey("torders"), nullable=False)
    TruckNumber = db.Column(db.String(20))
    LoadsDispatched = db.Column(db.Integer)

    order = relationship("Order")
