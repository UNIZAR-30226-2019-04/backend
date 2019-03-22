from .. import db

class Multimedia(db.Model):
    __tablename__ = "Multimedia"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Path = db.Column(db.String(255), nullable=False)
    Producto_ID = db.Column(db.Integer, db.ForeignKey("Producto.ID"), cascade="delete")


    def __repr__(self):
        return "<Multimedia '{}'>".format(self.Path)
