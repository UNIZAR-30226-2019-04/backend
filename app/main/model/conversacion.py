
from .. import db, flask_bcrypt
import datetime
from app.main.model.user import User
from ..config import key
import jwt


class Conversacion(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "conversacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    seller = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'),
                       nullable=False)
    seller_email = db.Column(db.String(65), unique=False, nullable=False)
    buyer = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'),
                      nullable=False)
    buyer_email = db.Column(db.String(65), unique=False, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "{} - {}".format(self.seller, self.buyer)
