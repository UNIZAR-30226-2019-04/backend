from flask_restplus import Namespace, fields

import datetime


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
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
