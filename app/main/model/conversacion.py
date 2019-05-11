from .. import db, flask_bcrypt
import datetime
from app.main.model.usuario import Usuario
from ..config import key
import jwt


class Conversacion(db.Model):
    __tablename__ = "conversacion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendedor = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete='CASCADE'), nullable=False)
    email_vendedor = db.Column(db.String(65), unique=False, nullable=False)
    comprador = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete='CASCADE'), nullable=False)
    email_comprador = db.Column(db.String(65), unique=False, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "{} - {}".format(self.vendedor, self.comprador)