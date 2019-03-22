from .. import db


class Producto(db.Model):
    __tablename__ = "Producto"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Precio = db.Column(db.Float, nullable=False)
    Descripcion = db.Column(db.Text, nullable=False, default='')
    Titulo = db.Column(db.String(255), nullable=False)
    NVisualizaciones = db.Column(db.Integer, nullable=False, default=0)
    Ubicacion = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    Paypal = db.Column(db.Boolean, nullable=True)
    Vendedor = db.Column(db.String(20), db.ForeignKey("Usuario.Nick"), nullable=False)
    Comprador = db.Column(db.String(20), db.ForeignKey("Usuario.Nick"), nullable=True)
    Borrado = db.Column(db.Borrado, nullable=False, default=False)

    def __repr__(self):
        return "<Producto '{}'>".format(self.Titulo)
