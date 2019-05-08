from sqlalchemy import text

from app.main import db
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from app.main.model.valoracion import Valoracion


def save_new_valoracion(user_id, auth, data):
    resp = Usuario.decode_auth_token(auth)
    user_token = Usuario.query.filter_by(id=resp).first()
    user = Usuario.query.filter_by(public_id=user_id).first()
    if user_token == user:
        producto = Producto.query.filter_by(id=data['puntuado']).first()
        if not user or not producto:
            response_object = {
                'status': 'fail',
                'message': 'Usuario o producto no existen',
            }
            return response_object, 404
        else:
            query = "SELECT MAX(id) FROM valoracion"
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
            new_valoracion = Valoracion(
                id=ind,
                descripcion=data['descripcion'],
                puntuacion=data['puntuacion'],
                puntuador=user.id,
                puntuado=producto.id,
            )
            save_changes(new_valoracion)
            response_object = {
                'status': 'success',
                'message': 'Valoración creada',
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
