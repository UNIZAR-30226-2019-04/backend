import uuid
import datetime

from app.main import db
from app.main.model.mensaje import Mensaje


def save_new_mensaje(data):

    new = Mensaje(
        emisor=data['emisor'],
        receptor=data['emisor'],
        text=data['text'],
        fecha=datetime.datetime.utcnow()
    )
    id = save_changes(new)
    response_object = {
        'status': 'success',
        'message': 'Successfully saved.',
    }
    return id


def get_all_mensajes():
    return Mensaje.query.all()


def get_a_mensaje(id):
    return Mensaje.query.filter_by(id=id).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
    return data
