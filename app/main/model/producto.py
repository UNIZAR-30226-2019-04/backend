from .. import db
import datetime
# from geoalchemy2 import Geography


class Producto(db.Model):
    __tablename__ = "Producto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text, nullable=False, default='')
    titulo = db.Column(db.String(255), nullable=False)
    visualizaciones = db.Column(db.Integer, nullable=False, default=0)
    # Ubicacion = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    paypal = db.Column(db.Boolean, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    vendedor = db.Column(db.Integer, db.ForeignKey("Usuario.id"), nullable=False)
    comprador = db.Column(db.Integer, db.ForeignKey("Usuario.id"), nullable=True)
    borrado = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<Producto '{}'>".format(self.titulo)
