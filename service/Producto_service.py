from model.Producto import Producto
from .. import db


def insertar_producto(data):
    new_producto = Producto(
        Precio=data['Precio'],
        Descripcion=data['Descripcion'],
        Titulo=data['Titulo'],
        Password=data['Password'],
        Ubicacion=data['Ubicacion'],
        Vendedor=data['Vendedor']
    )
    save_changes(new_producto)
    # TODO: ¿return?


def get_producto(id_producto):
    return Producto.query.filter_by(ID=id_producto).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
