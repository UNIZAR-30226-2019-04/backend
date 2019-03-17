from .. import db

class Producto(db.Model):
    __tablename__ = "Producto"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Precio = db.Column(db.Float, nullable=False)
    Descripcion = db.Column(db.String(255), nullable=True)
    Titulo = db.Column(db.String(255), nullable=False)
    NVisualizaciones = db.Column(db.Integer, nullable=False)
    Ubicacion = db.Column(db.Float, nullable=False)
    Paypal = db.Column(db.Boolean, nullable=False)
    Vendedor = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), nullable=False)
    Comprador = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), nullable=True)


    def __repr__(self):
        return "<Producto '{}'>".format(self.Titulo)
