from .. import db


class ReporteUsuario(db.Model):
    __tablename__ = "ReporteUsuario"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.Text, nullable=True)
    Tipo_de_reporte = db.Column(db.String(255), nullable=False)
    Reportado = db.Column(db.Integer, db.ForeignKey("Usuario.id"), primary_key=True)

    def __repr__(self):
        return "<ReporteUsuario '{}'>".format(self.Reportado)
