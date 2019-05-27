from .. import db


class CategoriaVisitada(db.Model):
    __tablename__ = "categoria_visitada"

    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    categoria_nombre = db.Column(db.String(30), db.ForeignKey("categoria.nombre"), primary_key=True)
    veces = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return "<Categoria visitada '{}'>".format(self.usuario)
