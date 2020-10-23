from app import db


class Jobs(db.Model):

    __tablename__ = 'tJobs'

    JobID = db.Column(db.Integer, primary_key=True)
    JobName = db.Column(db.String(100))
    JobStatus = db.Column(db.String(10))
