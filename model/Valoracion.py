from .. import db

class Valoracion(db.Model):
    __tablename__ = "Valoracion"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.String(255), nullable=True)
    Puntuacion = db.Column(db.Integer, nullable=False)
    Puntuador = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), primary_key=True)
    Puntuado = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), primary_key=True)


    def __repr__(self):
        return "<Valoracion '{}'>".format(self.Puntuacion)
