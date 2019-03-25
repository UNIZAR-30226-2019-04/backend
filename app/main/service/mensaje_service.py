import uuid
import datetime

from app.main import db
from app.main.model.Mensaje import Mensaje


def save_new_mensaje(data):

    new = Mensaje(
        Emisor=data['emisor'],
        Receptor=data['emisor'],
        Text=data['text'],
        Fecha=datetime.datetime.utcnow()
    )
    ID = save_changes(new)
    response_object = {
        'status': 'success',
        'message': 'Successfully saved.',
    }
    return ID


def get_all_mensajes():
    return Mensaje.query.all()


def get_a_mensaje(ID):
    return Mensaje.query.filter_by(ID=ID).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
    return data
