from .. import db


class Seguir(db.Model):
    __tablename__ = "seguir"

    seguidor = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    seguido = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

    def __repr__(self):
        return "<Seguir '{}'>".format(self.seguido)
