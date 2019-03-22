from model.Usuario import Usuario
from .. import db


# Auxiliar para la generación del token
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


def insertar_usuario(data):
    user_nick = Usuario.query.filter_by(Nick=data['Nick']).first()
    user_mail = Usuario.query.filter_by(email=data['email']).first()
    if not user_nick and not user_mail:
        new_user = Usuario(
            Nick=data['Nick'],
            Nombre=data['Nombre'],
            Apellidos=data['Apellidos'],
            email=data['email'],
            Password=data['Password'],
            # TODO: Al registrarse se podría añadir la típica checkbox: "Quiero recibir emails..."
            # quiereEmails=data['quiereEmails'],
            Ubicacion=data['Ubicacion'],
            Telefono=data['Telefono'],
            Imagen_Perfil_Path=data['Imagen_Perfil_Path']
        )
        save_changes(new_user)
        return generate_token(new_user)
    elif user_nick:
        response_object = {
            'status': 'fail',
            'message': 'Nickname already in use.',
        }
        return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'Email already in use.',
        }
        return response_object, 409


def get_all_users():
    return Usuario.query.all()


def get_a_user(nick=None, email=None):
    if nick:
        return Usuario.query.filter_by(Nick=nick).first()
    elif email:
        return Usuario.query.filter_by(email=email).first()
    else:
        raise ValueError('Expected either Nick or email args')


def get_user_id(nick=None, email=None):
    if nick:
        return Usuario.query.filter_by(Nick=nick).first().id
    elif email:
        return Usuario.query.filter_by(email=email).first().id
    else:
        raise ValueError('Expected either Nick or email args')


def save_changes(data):
    db.session.add(data)
    db.session.commit()
