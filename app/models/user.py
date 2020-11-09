from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.models.utils import ModelMixin


class User(db.Model, UserMixin, ModelMixin):

    __tablename__ = 'tUsers'

    UserID = db.Column(db.String(20), primary_key=True)
    FirstName = db.Column(db.String(25), nullable=False)
    LastName = db.Column(db.String(35), nullable=False)
    Initials = db.Column(db.String(5), nullable=False)
    Email = db.Column(db.String(100), nullable=False)
    Password = db.Column(db.String(50), nullable=False)

    def get_id(self):
        return self.UserID

    @hybrid_property
    def password(self):
        return self.Password

    @classmethod
    def authenticate(cls, UserID, Password):
        user = cls.query.filter(User.UserID == UserID).first()
        if user is not None and (user.Password == str.encode(Password)):
            return user

    def __str__(self):
        return '<User: %s>' % self.UserID


class AnonymousUser(AnonymousUserMixin):
    pass
