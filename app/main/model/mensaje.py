from .. import db
import datetime


class Mensaje(db.Model):
    __tablename__ = "mensaje"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    emisor = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    receptor = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

    def __repr__(self):
        return "<Mensaje '{}'>".format(self.text)
