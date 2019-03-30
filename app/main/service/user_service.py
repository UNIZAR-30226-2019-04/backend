import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from ..config import mailer


def save_new_user(data):
    user_nick = Usuario.query.filter_by(nick=data['username']).first()
    user_mail = Usuario.query.filter_by(email=data['email']).first()
    if not user_nick and not user_mail:
        new_user = Usuario(
            public_id=str(uuid.uuid4()),
            nick=data['username'],
            nombre=data['nombre'],
            apellidos=data['apellidos'],
            email=data['email'],
            password=data['password']
	        # TODO: Al registrarse se podría añadir la típica checkbox: "Quiero recibir emails..."
            # quiereEmails=data['quiereEmails'],
            # Ubicacion=data['Ubicacion'],
            # Telefono=data['telefono'],
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


def get_all_users():
    result = db.engine.execute("SELECT * FROM \"Usuario\";")
    response_object = []
    for usr in result:
        response_object.append({
            'username': usr[2],
            'email': usr[5],
            'public_id': usr[1],
            'password': usr[6],
        })
    return response_object


def get_a_user(public_id):
    response_object = {
        'username': Usuario.query.filter_by(public_id=public_id).first().nick,
        'email': Usuario.query.filter_by(public_id=public_id).first().email,
        'public_id': Usuario.query.filter_by(public_id=public_id).first().public_id,
        'password': Usuario.query.filter_by(public_id=public_id).first().password_hash,
    }
    return response_object

def get_user_id(nick=None, email=None):
    if nick:
        return Usuario.query.filter_by(nick=nick).first().id
    elif email:
        return Usuario.query.filter_by(email=email).first().id
    else:
        raise ValueError('Expected either nick or email args')

def get_user_NICK(email):
    return Usuario.query.filter_by(email=email).first().nick


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


def save_changes(data):
    db.session.add(data)
    db.session.commit()
