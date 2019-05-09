import uuid
import datetime

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from app.main.model.deseados import Deseados
from sqlalchemy import text


def save_new_deseado(user_id, auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=user_id).first()
    print(user_token)
    print(user)
    if user_token == user:
        producto = Producto.query.filter_by(id=data['producto_id']).first()
        if not user or not producto:
            response_object = {
                'status': 'fail',
                'message': 'Usuario o producto no existen',
            }
            return response_object, 404
        else:
            new_deseado = Deseados(
                usuario_id=user.id,
                producto_id=producto.id,
            )
            save_changes(new_deseado)
            response_object = {
                'status': 'success',
                'message': 'Producto añadido',
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Autorización no válida'
        }
        return response_object, 401


def remove_deseado(user_id, auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=user_id).first()
    print(user_token)
    print(user)
    if user_token == user:
        producto = Producto.query.filter_by(id=data['producto_id']).first()
        if not user or not producto:
            response_object = {
                'status': 'fail',
                'message': 'Usuario o producto no existen',
            }
            return response_object, 404
        else:
            Deseados.query.filter_by(usuario_id=user.id, producto_id=producto.id).delete()
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Producto eliminado de la lista',
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Autorización no válida'
        }
        return response_object, 401


def save_changes(data):
    db.session.add(data)
    db.session.commit()
