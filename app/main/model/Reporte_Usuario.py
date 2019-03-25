from .. import db

class Reporte_Usuario(db.Model):
    __tablename__ = "Reporte_Usuario"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.String(255), nullable=True)
    Tipo_de_reporte = db.Column(db.String(255), nullable=False)
    Reportado = db.Column(db.String(255), db.ForeignKey("Usuario.Nick"), primary_key=True)


    def __repr__(self):
        return "<Reporte_Usuario '{}'>".format(self.Reportado)
