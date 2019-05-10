from app.main import db
from app.main.model.multimedia import Multimedia


def get_multimedia():
    Multimedia.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
