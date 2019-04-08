import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from ..config import mailer

from geoalchemy2.types import WKTElement


def save_new_user(data):
    user_nick = Usuario.query.filter_by(nick=data['username']).first()
    user_mail = Usuario.query.filter_by(email=data['email']).first()
    if not user_nick and not user_mail:
        new_user = Usuario(
            public_id=str(uuid.uuid4()),
            nick=data['username'],
            # nombre=data['nombre'],
            # apellidos=data['apellidos'],
            email=data['email'],
            password=data['password'],
            # TODO: Al registrarse se podría añadir la típica checkbox: "Quiero recibir emails..."
            # quiereEmails=data['quiereEmails'],
            Ubicacion=WKTElement(data['Ubicacion'], srid=4326),
            RadioUbicacion=data['RadioUbicacion'],
            # telefono=data['telefono'],
            # Imagen_Perfil_Path=data['Imagen_Perfil_Path']
        )
        save_changes(new_user)
        send_confirmation_email(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def editar_usuario(public_id, data):
    user = Usuario.query.filter_by(public_id=public_id).first()
    if user:
        if 'nombre' in data:
            user.nombre = data['nombre']
        if 'apellidos' in data:
            user.apellidos = data['apellidos']
        if 'quiereEmails' in data:
            user.quiereEmails = data['quiereEmails']
        if 'telefono' in data:
            user.telefono = data['telefono']
        if 'Imagen_Perfil_Path' in data:
            user.Imagen_Perfil_Path = data['Imagen_Perfil_Path']
        # TODO: OJO
        if 'email' in data:
            user_mail = Usuario.query.filter_by(email=data['email']).first()
            if user_mail:
                response_object = {
                    'status': 'fail',
                    'message': 'Email already exists.',
                }
                return response_object, 409
            else:
                user.email = data['email']
        if 'nick' in data:
            user_nick = Usuario.query.filter_by(nick=data['nick']).first()
            if user_nick:
                response_object = {
                    'status': 'fail',
                    'message': 'Nick already exists.',
                }
                return response_object, 409
            else:
                user.nick = data['nick']
        save_changes(user)
        return user
    else:
        response_object = {
            'status': 'fail',
            'message': 'User not found.',
        }
        return response_object, 404


# TODO: Devuelve todos los usuarios de la base
def get_users():
    return Usuario.query.all()

# Recuperar un usuario dada su id publica
def get_a_user(public_id):
    return Usuario.query.filter_by(public_id=public_id).first()


# Recuperar la id publica de un usuario dado su nick o email
def get_user_id(nick=None, email=None):
    if nick:
        return Usuario.query.filter_by(nick=nick).first().public_id
    elif email:
        return Usuario.query.filter_by(email=email).first().public_id
    else:
        raise ValueError('Expected either nick or email args')


def get_user_products(public_id):
    usuario = Usuario.query.filter_by(public_id=public_id).first()
    return Producto.query.filter_by(vendedor=usuario.id).all()

def generate_token(user):
    try:
        # generate the auth token
        auth_token = Usuario.encode_auth_token(user.id)
        print(auth_token)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def send_confirmation_email(user):
    try:
        # generate the auth token
        confirmation_token = Usuario.encode_confirmation_token(user.email)
        mailer.send(
            subject='Bienvenido a Telocam - Confirmación de su correo electrónico',
            text_content=
            "Buenas " + user.nombre + " " + user.apellidos + ",\nconfirme su correo electrónico en la siguiente " +
            "dirección:\n" + confirmation_token + "\nSaludos,\nPaul Hodgetts\nDirector de Telocam",
            from_email='no-reply@telocam.com',
            to=[user.email]
        )
        response_object = {
            'status': 'success',
            'message': 'Successfully sent.',
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def confirm_user_email(public_id, token):
    try:
        user = get_a_user(public_id)
        if user.email == Usuario.decode_confirmation_token(token):
            user.validado = True
            response_object = {
                'status': 'success',
                'message': 'E-mail validado.'
            }
            return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def save_changes(data):
    db.session.add(data)
    db.session.commit()
