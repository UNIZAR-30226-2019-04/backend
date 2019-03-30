from .. import db


class Deseados(db.Model):
    __tablename__ = "Deseados"

    usuario_id = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey("Producto.id", ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return "<Deseados '{}'>".format(self.producto_id)
