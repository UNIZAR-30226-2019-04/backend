from .. import db

class Pertenece(db.Model):
    __tablename__ = "Pertenece"

    Producto_ID = db.Column(db.Integer, db.ForeignKey("Producto.ID"), primary_key=True)
    Categoria_Nombre = db.Column(db.String(255), db.ForeignKey("Categoria.Nombre"), primary_key=True)


    def __repr__(self):
        return "<Pertenece '{}'>".format(self.Categoria_Nombre)