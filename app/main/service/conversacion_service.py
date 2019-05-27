import uuid
import datetime

from app.main import db
from app.main.model.conversacion import Conversacion
from app.main.model.mensaje import Mensaje
from app.main.model.usuario import Usuario
from app.main.service.notification_service import send_push_message

from .user_service import get_user_id


def save_new_conversation(data):
    print("HOLA")
    vendedor = data['vendedor']
    vendedor2 = Usuario.query.filter_by(public_id=vendedor).first()
    comprador = data['comprador']
    if vendedor2.token:
        nombre = Usuario.query.filter_by(public_id=comprador).first().nick
        string = "El usuario " +  nombre + " quiere hablar contigo"
        send_push_message(vendedor2.token, string)
    chat = Conversacion.query.filter_by(
        vendedor = vendedor, comprador=comprador).first()
    chat2 = Conversacion.query.filter_by(
        vendedor = comprador, comprador = vendedor).first()
    if not chat and not chat2:
        new = Conversacion(
            vendedor=vendedor,
            comprador=comprador,
            email_vendedor=data['email_vendedor'],
            email_comprador=data['email_comprador'],
            fecha=datetime.datetime.utcnow()
        )
        save_changes(new)
        response_object = {
            'status': 'success',
            'message': 'Creada nueva conversación',
            'id': new.id,
        }
        return response_object, 200
    elif chat:
        response_object = {
            'status': 'success',
            'message': 'Conversacion already exists.',
            'id': chat.id,
        }
        return response_object, 200
    elif chat2:
        response_object = {
            'status': 'success',
            'message': 'Conversacion already exists.',
            'id': chat2.id,
        }
        return response_object, 200        


def get_all_conversations():
    return Conversacion.query.all()


def get_all_conversations_id(id):
    print(id)
    conversaciones_imagenes = []
    conversaciones = Conversacion.query.filter((Conversacion.vendedor == id) | (Conversacion.comprador == id)).all()
    print(conversaciones)
    for conversacion in conversaciones:
        print(conversacion)
        conversacion_imagen= {} 
        conversacion_imagen["id"] = conversacion.id
        conversacion_imagen["comprador"] = conversacion.comprador
        conversacion_imagen["vendedor"] = conversacion.vendedor
        conversacion_imagen["email_comprador"]= conversacion.email_comprador
        conversacion_imagen["email_vendedor"]= conversacion.email_vendedor
        imagen1 = Usuario.query.filter_by(public_id = conversacion.comprador).first().Imagen_Perfil_Path
        imagen2 = Usuario.query.filter_by(public_id = conversacion.vendedor).first().Imagen_Perfil_Path
        conversacion_imagen["imagen_comprador"]=imagen1
        conversacion_imagen["imagen_vendedor"]=imagen2
        convesaciones_imagenes = conversaciones_imagenes.append(conversacion_imagen)
    return conversaciones_imagenes

def get_all_conversations_id_id2(id,id2):
    print(id)
    return Conversacion.query.filter(((Conversacion.vendedor == id) & (Conversacion.comprador == id2))|((Conversacion.comprador == id) & (Conversacion.vendedor == id2)) ).all()



def get_a_conversation(id):
    return Conversacion.query.filter((Conversacion.vendedor == id) | (Conversacion.comprador == id)).first()


def get_conversation_mensajes(id):
    conver = Conversacion.query.filter_by(id=id).first()
    print(conver)
    if conver:
        messages = Mensaje.query.filter_by(conversacion=conver.id).all()
        print(messages)
        return messages
    else:
        response_object = {
            'status': 'fail',
            'message': 'La conversacion no existe.',
        }
        return 409


def save_changes(data):
    db.session.add(data)
    db.session.commit()
