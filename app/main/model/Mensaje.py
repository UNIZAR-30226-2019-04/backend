from .. import db
import datetime

class Producto(db.Model):
    __tablename__ = "Mensaje"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Text = db.Column(db.String(255), nullable=False)
    Fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    Emisor = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), primary_key=True)
    Receptor = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), primary_key=True)


    def __repr__(self):
        return "<Mensaje '{}'>".format(self.Text)
