from .. import db

class Usuario(db.Model):
    __tablename__ = "Usuario"

    Nick = db.Column(db.String(255), primary_key=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellidos = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    Validado = db.Column(db.Boolean, nullable=False, default=False)
    quiereEmails = db.Column(db.Boolean, nullable=False, default=True)
    Valoracion_Media = db.Column(db.Float, nullable=False, default=0.0)
    Ubicacion = db.Column(db.Float, nullable=False)
    Telefono = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        return "<Usuario '{}'>".format(self.Nick)
