from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.seguir import Seguir


def save_new_seguir(user_id, auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=user_id).first()
    if user_token == user:
        seguido = Usuario.query.filter_by(public_id=data['seguido']).first()
        if not user or not seguido:
            response_object = {
                'status': 'fail',
                'message': 'Usuario no válido',
            }
            return response_object, 404
        else:
            new_seguir = Seguir(
                seguidor=user.id,
                seguido=seguido.id
            )
            save_changes(new_seguir)
            response_object = {
                'status': 'success',
                'message': 'Usuario seguido',
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Autorización no válida'
        }
        return response_object, 401


def dejar_seguir(user_id, auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=user_id).first()
    if user_token == user:
        seguido = Usuario.query.filter_by(public_id=data['seguido']).first()
        if not user or not seguido:
            response_object = {
                'status': 'fail',
                'message': 'Usuario no válido',
            }
            return response_object, 404
        else:
            Seguir.query.filter_by(seguidor=user.id, seguido=seguido.id).delete()
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': 'Usuario dejado de seguir',
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
