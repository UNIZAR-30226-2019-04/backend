from app.main.model.producto import Producto
from app.main.model.pertenece import Pertenece
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


def get_products():
    return Producto.query.all()


def get_a_product(id_producto):
    if Producto.query.filter_by(id=producto).first():
        return Producto.query.filter_by(id=id_producto).first()
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def get_product_categories(id_producto):
    if Producto.query.filter_by(id=id_producto).first():
        per = Pertenece.query.filter_by(producto_id=id_producto).all()
        response_object = {
            'nombres': []
        }
        for cat in per:
            response_object['nombres'].append(cat.categoria_nombre)
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def add_categorias(producto, data):
    categorias = data['nombres']
    if Producto.query.filter_by(id=producto).first():
        for categoria in categorias:
            new_pertenece = Pertenece(
                producto_id=int(producto),
                categoria_nombre=categoria
            )
            save_changes(new_pertenece)
        response_object = {
            'status': 'success',
            'message': 'Categorías añadidas con éxito.',
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def save_changes(data):
    db.session.add(data)
    db.session.commit()
