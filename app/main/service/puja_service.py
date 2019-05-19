from sqlalchemy import text

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from app.main.model.puja import Puja


def save_new_puja(auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=data['usuario']).first()
    if user_token == user:
        pujado = Producto.query.filter_by(id=data['producto']).first()
        if not user or not pujado:
            response_object = {
                'status': 'fail',
                'message': 'Usuario o producto no válidos',
            }
            return response_object, 404
        else:
            query = "SELECT MAX(id) FROM puja"
            result = db.engine.execute(text(query))
            d, a = {}, []
            for row in result:
                # row.items() returns an array like [(key0, value0), (key1, value1)]
                for column, value in row.items():
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
            ind = a[0]['max']
            if ind is None:
                ind = 0
            ind += 1
            new_puja = Puja(
                id=ind,
                usuario=user.id,
                producto=pujado.id,
                valor=data['valor']
            )
            save_changes(new_puja)
            response_object = {
                'status': 'success',
                'message': 'Puja creada',
            }
            return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Autorización no válida'
        }
        return response_object, 401


def get_pujas(producto):
    prod = Producto.query.filter_by(id=producto).first()
    if prod:
        res = []
        pujas = Puja.query.filter_by(producto=producto).all()
        for puja in pujas:
            res.append(
                {'usuario': Usuario.query.filter_by(id=puja.usuario).first().public_id,
                 'producto': puja.producto,
                 'valor': puja.valor,
                 'fecha': puja.fecha})
        return res
    else:
        response_object = {
            'status': 'fail',
            'message': 'Producto no válido',
        }
        return response_object, 404


def save_changes(data):
    db.session.add(data)
    db.session.commit()
