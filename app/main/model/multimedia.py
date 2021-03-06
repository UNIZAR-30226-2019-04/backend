from app.main import db


class Multimedia(db.Model):
    __tablename__ = "multimedia"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Boolean, nullable=False)
    producto = db.Column(db.Integer, db.ForeignKey("producto.id"), nullable=False)

    def __repr__(self):
        return "<Multimedia '{}'>".format(self.path)
