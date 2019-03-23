from .. import db


class Valoracion(db.Model):
    __tablename__ = "Valoracion"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.Text, nullable=True)
    Puntuacion = db.Column(db.Integer, nullable=False)
    Puntuador = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True)
    Puntuado = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True)

    def __repr__(self):
        return "<Valoracion '{}'>".format(self.Puntuacion)
