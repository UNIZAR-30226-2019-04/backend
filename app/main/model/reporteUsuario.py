from .. import db


class ReporteUsuario(db.Model):
    __tablename__ = "reporte_usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text, nullable=True)
    tipoReporte = db.Column(db.String(255), nullable=False)
    reportado = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

    def __repr__(self):
        return "<ReporteUsuario '{}'>".format(self.reportado)
