from .. import db


class ReporteProducto(db.Model):
    __tablename__ = "ReporteProducto"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Descripcion = db.Column(db.Text, nullable=True)
    Tipo_de_reporte = db.Column(db.String(255), nullable=False)
    Reportado = db.Column(db.Integer, db.ForeignKey("Producto.ID"), primary_key=True, cascade="delete")

    def __repr__(self):
        return "<ReporteProducto '{}'>".format(self.Reportado)
