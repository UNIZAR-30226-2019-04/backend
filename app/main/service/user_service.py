import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from app.main.model.valoracion import Valoracion
from app.main.service.generar_email import generateEmail
from ..config import mailer
from sqlalchemy import text

# from geoalchemy2.types import WKTElement


def save_new_user(data):
    user_nick = Usuario.query.filter_by(nick=data['username']).first()
    user_mail = Usuario.query.filter_by(email=data['email']).first()
    if not user_nick and not user_mail:
        new_user = Usuario(
            public_id=str(uuid.uuid4()),
            nick=data['username'],
            email=data['email'],
            password=data['password'],
            # TODO: Al registrarse se podría añadir la típica checkbox: "Quiero recibir emails..."
            # quiereEmails=data['quiereEmails'],
            # Ubicacion=WKTElement(data['Ubicacion'], srid=4326),
            # radioUbicacion=data['radioUbicacion'],
        )
        save_changes(new_user)
        send_confirmation_email(new_user)
        return generate_token(new_user)
    elif user_mail:
        response_object = {
            'status': 'fail',
            'message': 'El email ya está en uso',
        }
        return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'El nombre de usuario ya está en uso',
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
        if 'descripcion' in data:
            user.descripcion = data['descripcion']
        # TODO: ¿SE PUEDE EDITAR EL MAIL?
        if 'email' in data and user.email != data['email']:
            user_mail = Usuario.query.filter_by(email=data['email']).first()
            if user_mail:
                response_object = {
                    'status': 'fail',
                    'message': 'El email ya está en uso.',
                }
                return response_object, 409
            else:
                user.email = data['email']
        if 'nick' in data and user.nick != data['nick']:
            user_nick = Usuario.query.filter_by(nick=data['nick']).first()
            if user_nick:
                response_object = {
                    'status': 'fail',
                    'message': 'El nombre de usuario ya está en uso.',
                }
                return response_object, 409
            else:
                user.nick = data['nick']
        # TODO: UBICACIÓN
        save_changes(user)
        return user
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def get_users():
    return Usuario.query.all()


# Recuperar un usuario dada su id publica
def get_a_user(public_id):
    user = Usuario.query.filter_by(public_id=public_id).first()
    if user:
        response_object = {
            'nick': user.nick,
            'descripcion': user.descripcion,
            'valoraciones_hechas': [],
            'valoraciones_recibidas': [],
            'cajas_productos': [],
        }

        id_usr = user.id
        query_args = {}
        # Productos vendidos por el usuario
        query = "SELECT COUNT(*) FROM producto WHERE vendedor = :id AND comprador IS NOT NULL"
        query_args['id'] = id_usr
        result = db.engine.execute(text(query), query_args)
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                response_object['productos_vendidos'] = value

        # Productos comprados por el usuario
        query = "SELECT COUNT(*) FROM producto WHERE comprador = :id"
        result = db.engine.execute(text(query), query_args)
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                response_object['productos_comprados'] = value

        # Productos que el usuario tiene a la venta
        productos = Producto.query.filter_by(vendedor=id_usr).filter_by(comprador=None).all()
        for p in productos:
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'vendedor': p.vendedor,
                'tipo': p.tipo,
            }
            response_object['cajas_productos'].append(producto)

        # Productos en la lista de deseados del usuario
        query = "SELECT p.id, p.\"precioBase\", p.\"precioAux\", p.descripcion, p.titulo, p.visualizaciones, p.fecha, p.vendedor, p.tipo FROM producto AS p, deseados as d WHERE p.id = d.producto_id AND d.usuario_id = :id"
        result = db.engine.execute(text(query), query_args)
        d, a = {}, []
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                d = {**d, **{column: value}}
            a.append(d)
        response_object['deseados'] = a

        # Valoraciones hechas por el usuario
        valoraciones_hechas = Valoracion.query.filter_by(puntuador=id_usr).all()
        for v in valoraciones_hechas:
            valoracion = {
                'descripcion': v.descripcion,
                'puntuacion': v.puntuacion,
                'puntuador': user.nick,
                'puntuado': Usuario.query.filter_by(id=v.puntuado).first().nick,
            }
            response_object['valoraciones_hechas'].append(valoracion)

        # Valoraciones recibidas por el usuario
        valoraciones_recibidas = Valoracion.query.filter_by(puntuado=id_usr).all()
        for v in valoraciones_recibidas:
            valoracion = {
                'descripcion': v.descripcion,
                'puntuacion': v.puntuacion,
                'puntuador': Usuario.query.filter_by(id=v.puntuador).first().nick,
                'puntuado': user.nick,
            }
            response_object['valoraciones_recibidas'].append(valoracion)
        #print(response_object)
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


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
    print(usuario)
    if usuario:
        response_object = {
            'cajas_productos': [],
        }
        productos = Producto.query.filter_by(vendedor=usuario.id).all()
        for p in productos:
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'vendedor': p.vendedor,
                'tipo': p.tipo,
            }
            response_object['cajas_productos'].append(producto)
        return response_object
    else:
        print("NOUSUARIO")
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


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
    print("Enviar email")
    try:
        # generate the auth token
        confirmation_token = Usuario.encode_confirmation_token(user.email)
        html_email = generateEmail(user.nick, confirmation_token)
        mailer.send(
            subject='Bienvenido a Telocam - Confirmación de su correo electrónico',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[user.email]
        )
        response_object = {
            'status': 'success',
            'message': 'Successfully sent.',
        }
        print(response_object)
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        print(response_object, e)
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
