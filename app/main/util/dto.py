from flask_restplus import Namespace, fields

import datetime


# 'password': fields.String(required=True, description='user password'), GENERA CONFLICTO
class UserDto:
    api = Namespace('user', description='Operaciones sobre usuarios')
    user = api.model('user', {
        'public_id': fields.String(description='Id publico del usuario'),
        'nick': fields.String(description='Nick del usuario'),
        'nombre': fields.String(description='Nombre del usuario'),
        'apellidos': fields.String(description='Apellidos del usuario'),
        'email': fields.String(required=True, description='email del usuario'),
        'quiereEMails': fields.Boolean(description='True si el usuario desea recibir emails, False en caso contrario'),
        'valoracionMedia': fields.Float(description='Valoración media del usuario'),
        'telefono': fields.Integer(description='Teléfono del usuario'),
        'Imagen_Perfil_Path': fields.String(description='Foto de perfil del usuario')
        # 'Ubicacion': fields.String(description='Ubicación. Formato POINT(<lon> <lat>), ejemplo: \'POINT(3.0 -2.3)\''),
        # 'radioUbicacion': fields.Integer(description='Radio en metros de la ubicación')
    })
    user_reg = api.model('user', {
        'nick': fields.String(description='Nick del usuario'),
        'email': fields.String(required=True, description='email del usuario'),
    })


class CategoriaDto:
    api = Namespace('categoria', description='categoria related operations')
    categoria = api.model('categoria', {
        'nombre': fields.String(required=True, description='nombre de categoria')
    })


class CategoriaListaDto:
    api = Namespace('categoriaLista', description='categoriaLista related operations')
    categoriaLista = api.model('categoriaLista', {
        'nombres': fields.List(fields.String, required=True, description='nombres de categorias')
    })


class ProductoDto:
    api = Namespace('producto', description='producto related operations')
    producto = api.model('producto', {
        'id': fields.Integer(description='id del producto'),
        'precioBase': fields.Float(required=True, description='precio base del producto'),
        'precioAux': fields.Float(description='precio actual de la subasta o maximo del trueque'),
        'descripcion': fields.String(required=True, description='descripcion del producto'),
        'titulo': fields.String(required=True, description='nombre del producto'),
        'visualizaciones': fields.Integer(description='numero de visualizaciones del producto'),
        'fecha': fields.DateTime(description='fecha de creacion del producto'),
        'vendedor': fields.Integer(required=True, description='vendedor del producto'),
        'tipo': fields.String(required=True, description='venta, trueque o subasta')
        # 'Ubicacion': fields.String(description='Ubicación. Formato POINT(<lon> <lat>), ejemplo: \'POINT(3.0 -2.3)\''),
        # 'radioUbicacion': fields.Integer(description='Radio en metros de la ubicación')
    })


class ConversationDto:
    api = Namespace(
        'conversacion', description='conversacion related operations')
    conversacion = api.model('conversacion', {
        'id': fields.Integer(required=True, description='id'),
        'seller': fields.Integer(required=True, description='seller id'),
        'buyer': fields.Integer(required=True, description='buyer id'),
        'seller_email': fields.String(required=True, description='seller email'),
        'buyer_email': fields.String(required=True, description='buyer email'),

    })


class MensajeDto:
    api = Namespace(
        'mensaje', description='mensaje related operations')
    mensaje = api.model('mensaje', {
        'id': fields.Integer(required=True, description='id'),
        'conversacion': fields.Integer(required=True, description='conversacion id'),
        'text': fields.String(required=True, description='text'),
        'user': fields.String(required=True, description='user'),
        'created_date': fields.DateTime(required=True, description='created_date'),

    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='Email o username'),
        'password': fields.String(required=True, description='Contraseña'),
    })


class GeocodeDto:
    api = Namespace('geocode', description='Operaciones de geocodificación')
