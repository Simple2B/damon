from app import db


class Customer(db.Model):

    __tablename__ = 'tCustomer'

    CustomerID = db.Column(db.Integer, primary_key=True)
    CustomerName = db.Column(db.String(50))
