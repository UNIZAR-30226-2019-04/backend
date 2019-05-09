import datetime
from datetime import datetime

from sqlalchemy import text
from app.main.model.producto import Producto
from app.main.model.usuario import Usuario
from app.main.model.pertenece import Pertenece
from .. import db


def insertar_producto(data):
    usuario = Usuario.query.filter_by(public_id=data['vendedor']).first()
    if usuario:
        new_producto = Producto(
            precioBase=data['precioBase'],
            descripcion=data['descripcion'],
            titulo=data['titulo'],
            vendedor=usuario.id,
            tipo=data['tipo']
        )
        if 'precioAux' in data:
            new_producto.precioAux=data['precioAux']
        if 'fechaexpiracion' in data:
            new_producto.fechaexpiracion = data['fechaexpiracion']
        if 'latitud' in data:
            new_producto.latitud=data['latitud']
            new_producto.longitud=data['longitud']
            new_producto.radio_ubicacion=data['radio_ubicacion']
        else:
            if usuario.latitud is not None:
                new_producto.latitud = usuario.latitud
                new_producto.longitud = usuario.longitud
                new_producto.radio_ubicacion = usuario.radio_ubicacion
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'El usuario o el producto deben tener ubicación.',
                }
                return response_object
        save_changes(new_producto)
        new_pertenece = Pertenece(
            producto_id=new_producto.id,
            categoria_nombre=data['categoria']
        )
        save_changes(new_pertenece)
        response_object = {
            'status': 'success',
            'message': 'Producto creado.',
            'id': new_producto.id,
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Usuario no válido.',
        }
        return response_object


def editar_producto(id, data):
    producto = Producto.query.filter_by(id=id, borrado=False).first()
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


# TODO: Formatear la fecha, quizá sea necesario hacer la consulta a mano
def get_a_product(id_producto):
    producto = Producto.query.filter_by(id=id_producto, borrado=False).first()

    if producto:
        producto.visualizaciones += 1
        save_changes(producto)
        response_object = {
            'id': producto.id,
            'precioBase': producto.precioBase,
            'precioAux': producto.precioAux,
            'descripcion': producto.descripcion,
            'titulo': producto.titulo,
            'visualizaciones': producto.visualizaciones,
            'fecha': producto.fecha.strftime('%d/%m/%Y'),
            'fechaexpiracion': producto.fechaexpiracion.strftime('%d/%m/%Y'),
            'latitud': producto.latitud,
            'longitud': producto.longitud,
            'radio_ubicacion': producto.radio_ubicacion,
            'vendedor': Usuario.query.filter_by(id=producto.vendedor).first().public_id,
            'tipo': producto.tipo,
            'categoria': Pertenece.query.filter_by(producto_id=producto.id).first().categoria_nombre
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


# TODO: Completar con los parámetros que se quiera
# def search_products(textoBusqueda, preciomin, preciomax, ubicacion, radioUbicacion, valoracionMin, valoracionMax):
def search_products(number=None, page=None, textobusqueda=None, preciomin=None, preciomax=None, tipocompra=None,
                    valoracionMin=None, valoracionMax=None, categorias=None, latitud=None, longitud=None, radio=None):
    query_args = {}
    query = "SELECT p.id, p.\"precioBase\", p.\"precioAux\", p.descripcion, p.titulo, p.visualizaciones, p.fecha, " \
            "p.vendedor, p.tipo, pe.categoria_nombre FROM producto AS p, pertenece AS pe"
    numpars = 0
    # Sección para joins
    if valoracionMin or valoracionMax:
        query += ", usuario AS u WHERE "
        if valoracionMin:
            query += "(u.id = p.vendedor AND u.valoracion_media >= :valoracionMin)"
            numpars += 1
            query_args['valoracionMin'] = valoracionMin
        if valoracionMax:
            if numpars != 0:
                query += " AND "
            query += "(u.id = p.vendedor AND u.valoracion_media <= :valoracionMax)"
            numpars += 1
            query_args['valoracionMax'] = valoracionMax
    if categorias:
        tam = len(categorias)
        cat = "categoria_nombre"
        if numpars != 0:
            query += " AND"
        else:
            query += " WHERE"
        numpars +=1
        query += " (pe.categoria_nombre = :categoria_nombre0"
        query_args['categoria_nombre0'] = categorias[0]
        for i in range(1, tam):
            query += " OR pe.categoria_nombre = :categoria_nombre" + str(i)
            query_args['categoria_nombre'+str(i)] = categorias[i]
        query += ")"
    # Sección para comprobaciones no join
    if numpars == 0:
        query += " WHERE"
    else:
        query += " AND"
    query += " p.borrado = false AND p.comprador IS NULL AND pe.producto_id = p.id"
    # TODO: Pensar bien cómo hacer esta búsqueda, ¿número de apariciones del string?, ¿tiene más peso si aparece en el título?, ...
    if textobusqueda:
        textobusqueda = "%" + textobusqueda + "%"
        query += " AND (p.titulo LIKE :textobusqueda OR p.descripcion LIKE :textobusqueda)"
        query_args['textobusqueda'] = textobusqueda
    if preciomin:
        query += " AND p.\"precioBase\" >= :preciomin"
        query_args['preciomin'] = preciomin
    if preciomax:
        query += " AND p.\"precioBase\" <= :preciomax"
        query_args['preciomax'] = preciomax
    if tipocompra:
        query += " AND p.tipo = :tipocompra"
        query_args['tipocompra'] = tipocompra
    if latitud:
        query += " AND calcular_distancia(p.latitud, p.longitud, p.radio_ubicacion, :latitud, :longitud, :radio) <= 0"
        query_args['latitud'] = latitud
        query_args['longitud'] = longitud
        query_args['radio'] = radio
    query += " LIMIT :number OFFSET :page"
    query_args['number'] = number
    query_args['page'] = page*number
    print(query)
    result = db.engine.execute(text(query), query_args)
    d, a = {}, []
    for row in result:
        # row.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in row.items():
            # build up the dictionary
            if isinstance(value, datetime):
                value = value.strftime('%d/%m/%Y')
            d = {**d, **{column: value}}
        a.append(d)
    return a


def get_product_categories(id_producto):
    if Producto.query.filter_by(id=id_producto, borrado=False).first():
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
    if Producto.query.filter_by(id=producto, borrado=False).first():
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
