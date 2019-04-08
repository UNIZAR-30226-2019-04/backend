from .. import db
import datetime
from geoalchemy2 import Geometry
from sqlalchemy.dialects.postgresql import ENUM


class Producto(db.Model):
    __tablename__ = "Producto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    precioBase = db.Column(db.Float, nullable=False)
    # Para trueques será el valor máximo, para subastas el precio actual
    precioAux = db.Column(db.Float, nullable=True)
    descripcion = db.Column(db.Text, nullable=False, default='')
    titulo = db.Column(db.String(255), nullable=False)
    visualizaciones = db.Column(db.Integer, nullable=False, default=0)
    Ubicacion = db.Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    radioUbicacion = db.Column(db.Integer, nullable=False, default=0)
    paypal = db.Column(db.Boolean, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    vendedor = db.Column(db.Integer, db.ForeignKey("Usuario.id"), nullable=False)
    comprador = db.Column(db.Integer, db.ForeignKey("Usuario.id"), nullable=True)
    borrado = db.Column(db.Boolean, nullable=False, default=False)
    tipo = db.Column(ENUM('normal', 'trueque', 'subasta', name='tipoProducto'), nullable=False, default='normal')

    def __repr__(self):
        return "<Producto '{}'>".format(self.titulo)
