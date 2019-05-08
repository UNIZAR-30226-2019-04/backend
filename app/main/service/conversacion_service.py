import uuid
import datetime

from app.main import db
from app.main.model.conversacion import Conversacion
from app.main.model.mensaje import Mensaje

from .user_service import get_user_id


def save_new_conversation(data):
    chat = Conversacion.query.filter_by(
        vendedor=data['vendedor'], comprador=data['comprador']).first()
    if not chat:
        new = Conversacion(
            id=data['id'],
            vendedor=data['vendedor'],
            comprador=data['comprador'],
            email_vendedor=data['email_vendedor'],
            email_comprador=data['email_comprador'],
            created_date=datetime.datetime.utcnow()
        )
        save_changes(new)
        response_object = {
            'status': 'success',
            'message': 'Successfully saved.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Conversacion already exists. Please Log in.',
        }
        return response_object, 409


def get_all_conversations():
    return Conversacion.query.all()


def get_all_conversations_id(email):
    id = get_user_id(email)
    print(id)
    return Conversacion.query.filter((Conversacion.vendedor == id) | (Conversacion.comprador == id)).all()


def get_a_conversation(id):
    return Conversacion.query.filter((Conversacion.vendedor == id) | (Conversacion.comprador == id)).first()


def get_conversation_mensajes(id):
    conver = Conversacion.query.filter_by(id=id).first()
    print(conver)
    messages = Mensaje.query.filter_by(conversacion=conver.id).all()
    print(messages)
    return messages


def save_changes(data):
    db.session.add(data)
    db.session.commit()