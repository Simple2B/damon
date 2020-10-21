from app import db


class Materials(db.Model):

    __tablename__ = 'tMaterials'

    MaterialID = db.Column(db.Integer, primary_key=True)
    MaterialName = db.Column(db.String(20))
