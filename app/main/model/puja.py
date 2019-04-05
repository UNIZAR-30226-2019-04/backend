from .. import db
import datetime


class Puja(db.Model):
    __tablename__ = "Puja"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True)
    producto = db.Column(db.Integer, db.ForeignKey("Producto.id"), primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return "<Puja '{}'>".format(self.reportado)
