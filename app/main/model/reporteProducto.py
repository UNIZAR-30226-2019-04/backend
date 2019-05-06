from .. import db


class ReporteProducto(db.Model):
    __tablename__ = "reporte_producto"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text, nullable=True)
    tipoReporte = db.Column(db.String(255), nullable=False)
    reportado = db.Column(db.Integer, db.ForeignKey("producto.id", ondelete='CASCADE'), primary_key=True)

    def __repr__(self):
        return "<ReporteProducto '{}'>".format(self.reportado)
