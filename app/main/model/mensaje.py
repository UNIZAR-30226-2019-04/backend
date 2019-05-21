from .. import db
import datetime


class Mensaje(db.Model):
    __tablename__ = "mensaje"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    texto = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    conversacion = db.Column(db.Integer, db.ForeignKey("conversacion.id", ondelete='CASCADE'), nullable=False)
    usuario = db.Column(db.String(100), db.ForeignKey("usuario.public_id", ondelete='CASCADE'), nullable=False)
    # emisor = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    # receptor = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

    def __repr__(self):
        return "<Mensaje '{}'>".format(self.texto)
