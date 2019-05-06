from .. import db


class Categoria(db.Model):
    __tablename__ = "categoria"

    nombre = db.Column(db.String(30), primary_key=True)

    def __repr__(self):
        return "<Categoria '{}'>".format(self.nombre)
