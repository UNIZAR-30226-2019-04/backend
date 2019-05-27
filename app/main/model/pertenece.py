from .. import db


class Pertenece(db.Model):
    __tablename__ = "pertenece"

    producto_id = db.Column(db.Integer, db.ForeignKey("producto.id", ondelete='CASCADE'), primary_key=True)
    categoria_nombre = db.Column(db.String(30), db.ForeignKey("categoria.nombre"), primary_key=True)

    def __repr__(self):
        return "<Pertenece '{}'>".format(self.categoria_nombre)
