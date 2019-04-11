from geoalchemy2 import WKTElement
from sqlalchemy import text
from app.main.model.producto import Producto
from app.main.model.pertenece import Pertenece
from .. import db


def insertar_producto(data):
    new_producto = Producto(
        precioBase=data['precioBase'],
        descripcion=data['descripcion'],
        titulo=data['titulo'],
        Ubicacion=WKTElement('POINT({0} {1})'.format(data['lon'], data['lat']), srid=4326),
        RadioUbicacion=data['RadioUbicacion'],
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


# TODO: Completar con los parámetros que se quiera (los joins requieren trabajo adicional)
# def search_products(textoBusqueda, preciomin, preciomax, ubicacion, radioUbicacion, valoracionMin, valoracionMax):
def search_products(textobusqueda=None, preciomin=None, preciomax=None):
    query_args = {}
    query = "SELECT * FROM \"Producto\" WHERE "
    numpars = 0
    # TODO: Pensar bien cómo hacer esta búsqueda, ¿número de apariciones del string?, ¿tiene más peso si aparece en el título?, ...
    if textobusqueda:
        textobusqueda = "%" + textobusqueda + "%"
        query += "(titulo LIKE :textobusqueda OR descripcion LIKE :textobusqueda)"
        numpars += 1
        query_args['textobusqueda'] = textobusqueda
    if preciomin:
        if numpars != 0:
            query += " AND "
        query += "\"precioBase\" >= :preciomin"
        numpars += 1
        query_args['preciomin'] = preciomin
    if preciomax:
        if numpars != 0:
            query += " AND "
        query += "\"precioBase\" <= :preciomax"
        numpars += 1
        query_args['preciomax'] = preciomax

    result = db.engine.execute(text(query), query_args)
    d, a = {}, []
    for row in result:
        # row.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in row.items():
            # build up the dictionary
            d = {**d, **{column: value}}
        a.append(d)
    return a


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
