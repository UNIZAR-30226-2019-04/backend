from .. import db


class Valoracion(db.Model):
    __tablename__ = "valoracion"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text, nullable=True)
    puntuacion = db.Column(db.Integer, nullable=False)
    puntuador = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    puntuado = db.Column(db.Integer, db.ForeignKey("producto.id"), primary_key=True)

    def __repr__(self):
        return "<Valoracion '{}'>".format(self.puntuacion)
