from .. import db


class Multimedia(db.Model):
    __tablename__ = "Multimedia"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(255), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("Producto.id"), cascade="delete")

    def __repr__(self):
        return "<Multimedia '{}'>".format(self.path)
