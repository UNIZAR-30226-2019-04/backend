from app.main.model.producto import Producto
from .. import db


def insertar_producto(data):
    new_producto = Producto(
        precio=data['precio'],
        descripcion=data['descripcion'],
        titulo=data['titulo'],
        # ubicacion=data['ubicacion'],
        vendedor=data['vendedor']
    )
    save_changes(new_producto)
    return {"Respuesta":"Return WIP, checkear manualmente si OK"}


def get_all_products():
    result = db.engine.execute("SELECT * FROM \"Producto\";")
    response_object = []
    for producto in result:
        response_object.append({
            'precio': producto[1],
            'titulo': producto[3],
            'descripcion': producto[2],
            'vendedor': producto[7],
            'fecha': producto[6],
        })
    return response_object


def get_producto(id_producto):
    response_object = {
        'precio': Producto.query.filter_by(id=id_producto).first().precio,
        'titulo': Producto.query.filter_by(id=id_producto).first().titulo,
        'descripcion': Producto.query.filter_by(id=id_producto).first().descripcion,
        'vendedor': Producto.query.filter_by(id=id_producto).first().vendedor,
        'fecha': Producto.query.filter_by(id=id_producto).first().fecha,
    }
    return response_object


def save_changes(data):
    db.session.add(data)
    db.session.commit()
