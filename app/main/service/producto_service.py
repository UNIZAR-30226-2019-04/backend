from app.main.model.producto import Producto
from .. import db


def insertar_producto(data):
    new_producto = Producto(
        precioBase=data['precioBase'],
        descripcion=data['descripcion'],
        titulo=data['titulo'],
        # ubicacion=data['ubicacion'],
        vendedor=data['vendedor'],
        tipo=data['tipo']
    )
    if 'precioAux' in data:
        new_producto.precioAux=data['precioAux']
    save_changes(new_producto)
    return {"Respuesta":"Return WIP, checkear manualmente si OK"}


def editar_producto(id, data):
    producto = Producto.query.filter_by(id=id).first()
    if producto:
        if 'descripcion' in data:
            producto.descripcion = data['descripcion']
        if 'titulo' in data:
            producto.titulo = data['titulo']
        save_changes(producto)
        return producto
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def get_all_products():
    result = db.engine.execute("SELECT * FROM \"Producto\";")
    response_object = []
    for producto in result:
        response_object.append({
            'precioBase': producto[1],
            'titulo': producto[3],
            'descripcion': producto[2],
            'vendedor': producto[7],
            'fecha': producto[6],
        })
    return response_object


def get_products():
    return Producto.query.all()

def get_a_product(id_producto):
    return Producto.query.filter_by(id=id_producto).first()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
