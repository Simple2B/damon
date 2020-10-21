from app import db


class Trucks(db.Model):

    __tablename__ = 'tTrucks'

    TruckID = db.Column(db.Integer, primary_key=True)
    SubcontractorID = db.Column(db.Integer)
    TruckNumber = db.Column()
    OwnedTruck = db.Column()
    TruckPercentage = db.Column()
    IsActive = db.Column()