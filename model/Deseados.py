from .. import db

class Deseados(db.Model):
    __tablename__ = "Deseados"

    Usuario_Nick = db.Column(db.String(20), db.ForeignKey("Usuario.Nick"), primary_key=True)
    Producto_ID = db.Column(db.Integer, db.ForeignKey("Producto.ID"), primary_key=True, cascade="delete")


    def __repr__(self):
        return "<Deseados '{}'>".format(self.Producto_ID)
