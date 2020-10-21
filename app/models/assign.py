from app import db
from app.models.utils import ModelMixin


class Assign(db.Model, ModelMixin):

    __tablename__ = 'tassign'

    assignID = db.Column(db.Integer, primary_key=True)
    TicketID = db.Column(db.Integer, nullable=False)
    Loads = db.Column(db.String(20))
    Status = db.Column(db.String(9))
