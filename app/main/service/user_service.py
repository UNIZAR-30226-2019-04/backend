import uuid
import datetime

from app.main import db
from app.main.model.Usuario import Usuario
from ..config import mailer


def save_new_user(data):
    user = Usuario.query.filter_by(email=data['email']).first()
    if not user:
        new_user = Usuario(
            Nick=data['username'],
            Nombre=data['nombre'],
            Apellidos=data['apellidos'],
            email=data['email'],
            password=data['password'],
            Telefono=data['telefono'],
            Validado=False
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
    return Usuario.query.all()


def get_a_user(Nick):
    return Usuario.query.filter_by(Nick=Nick).first()


def get_user_NICK(email):
    return Usuario.query.filter_by(email=email).first().Nick


def generate_token(user):
    try:
        # generate the auth token
        auth_token = Usuario.encode_auth_token(user.id)
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
            "Buenas " + user.Nombre + " " + user.Apellidos + ",\nconfirme su correo electrónico en la siguiente " +
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
