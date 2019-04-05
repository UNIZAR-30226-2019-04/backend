from flask_restplus import Namespace, fields

import datetime


# 'password': fields.String(required=True, description='user password'), GENERA CONFLICTO
class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'public_id': fields.String(description='id publico del usuario'),
        'nick': fields.String(description='nick del usuario'),
        'nombre': fields.String(description='nombre del usuario'),
        'apellidos': fields.String(description='apellidos del usuario'),
        'email': fields.String(required=True, description='email del usuario'),
        'quiereEMails': fields.Boolean(description='si el usuario desea recibir emails'),
        'valoracionMedia': fields.Float(description='valoracion media del usuario'),
        'telefono': fields.Integer(description='telefono del usuario'),
        'Imagen_Perfil_Path': fields.String(description='foto perfil del usuario')
    })


class ProductoDto:
    api = Namespace('producto', description='producto related operations')
    producto = api.model('poducto', {
        'precioBase': fields.Float(required=True, description='precio base del producto'),
        'precioAux': fields.Float(description='precio actual de la subasta o maximo del trueque'),
        'descripcion': fields.String(required=True, description='descripcion del producto'),
        'titulo': fields.String(required=True, description='nombre del producto'),
        'visualizaciones': fields.Integer(description='numero de visualizaciones del producto'),
        'fecha': fields.DateTime(description='fecha de creacion del producto'),
        'vendedor': fields.Integer(required=True, description='vendedor del producto'),
        'tipo': fields.Integer(required=True, description='venta, trueque o subasta')

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
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
