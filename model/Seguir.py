from .. import db

class Seguir(db.Model):
    __tablename__ = "Seguir"

    Seguidor = db.Column(db.String(20), db.ForeignKey("Usuario.Nick"), primary_key=True)
    Seguido = db.Column(db.String(20), db.ForeignKey("Usuario.Nick"), primary_key=True)


    def __repr__(self):
        return "<Seguir '{}'>".format(self.Seguido)
