
from .. import db, flask_bcrypt
import datetime
from app.main.model.conversacion import Conversacion
from ..config import key
import jwt


class Mensaje(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "mensaje"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversacion = db.Column(db.Integer, db.ForeignKey("conversacion.id", ondelete='CASCADE'),
                             nullable=False)
    text = db.Column(db.String(300), unique=False, nullable=False)

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user = db.Column(db.String(300),  nullable=False)

    def __repr__(self):
        return "Conversation: {} - User: {} - Text: {}".format(self.conversacion, self.user, self.text)
