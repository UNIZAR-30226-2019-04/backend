import datetime
from datetime import datetime

from sqlalchemy import text
from app.main.model.producto import Producto
from app.main.model.usuario import Usuario
from app.main.model.pertenece import Pertenece
from app.main.model.multimedia import Multimedia
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
        fechaexpiracion = producto.fechaexpiracion
        if fechaexpiracion is not None:
            fechaexpiracion = fechaexpiracion.strftime('%d/%m/%Y')
        multi = []
        for i in Multimedia.query.filter_by(producto=id_producto).all():
            multi.append({"path": i.path, "tipo": i.tipo})
        response_object = {
            'id': producto.id,
            'precioBase': producto.precioBase,
            'precioAux': producto.precioAux,
            'descripcion': producto.descripcion,
            'titulo': producto.titulo,
            'visualizaciones': producto.visualizaciones,
            'fecha': producto.fecha.strftime('%d/%m/%Y'),
            'fechaexpiracion': fechaexpiracion,
            'latitud': producto.latitud,
            'longitud': producto.longitud,
            'radio_ubicacion': producto.radio_ubicacion,
            'vendedor': Usuario.query.filter_by(id=producto.vendedor).first().public_id,
            'tipo': producto.tipo,
            'categoria': Pertenece.query.filter_by(producto_id=producto.id).first().categoria_nombre,
            'multimedia': multi
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
                    valoracionMin=None, valoracionMax=None, categorias=None, latitud=None, longitud=None, radio=None,
                    usuario=None):
    # TODO: MULTIMEDIA REAL
    multi = [{"path": "http://155.210.47.51:10080/logo.png", "tipo": False},
             {"path": "http://155.210.47.51:10080/giphy.mp4", "tipo": True}]

    query_args = {}
    numresquery = "SELECT COUNT(*)"
    query = "SELECT p.id, p.\"precioBase\", p.\"precioAux\", p.descripcion, p.titulo, p.visualizaciones, p.fecha, " \
            "v.public_id AS vendedor, p.tipo, pe.categoria_nombre,"
    if usuario:
        usr = Usuario.query.filter_by(public_id=usuario).first()
        if usr:
            query += " EXISTS(SELECT 1 FROM deseados d WHERE d.producto_id=p.id AND d.usuario_id=:usuario) AS deseado"
            query_args['usuario'] = usr.id
        else:
            response_object = {
                'status': 'fail',
                'message': 'El usuario no existe.',
            }
            return response_object, 404
    else:
        query += " false AS deseado"
    query += " FROM producto p, pertenece pe, usuario u, usuario v"
    numresquery += " FROM producto p, pertenece pe, usuario u, usuario v"
    numpars = 0
    # Sección para joins
    if valoracionMin or valoracionMax:
        query += " WHERE "
        numresquery += " WHERE "
        if valoracionMin:
            query += "(u.id = p.vendedor AND u.valoracion_media >= :valoracionMin)"
            numresquery += "(u.id = p.vendedor AND u.valoracion_media >= :valoracionMin)"
            numpars += 1
            query_args['valoracionMin'] = valoracionMin
        if valoracionMax:
            if numpars != 0:
                query += " AND "
                numresquery += " AND "
            query += "(u.id = p.vendedor AND u.valoracion_media <= :valoracionMax)"
            numresquery += "(u.id = p.vendedor AND u.valoracion_media <= :valoracionMax)"
            numpars += 1
            query_args['valoracionMax'] = valoracionMax
    if categorias:
        tam = len(categorias)
        if numpars != 0:
            query += " AND"
            numresquery += " AND"
        else:
            query += " WHERE"
            numresquery += " WHERE"
        numpars +=1
        query += " (pe.categoria_nombre = :categoria_nombre0"
        numresquery += " (pe.categoria_nombre = :categoria_nombre0"
        query_args['categoria_nombre0'] = categorias[0]
        for i in range(1, tam):
            query += " OR pe.categoria_nombre = :categoria_nombre" + str(i)
            numresquery += " OR pe.categoria_nombre = :categoria_nombre" + str(i)
            query_args['categoria_nombre'+str(i)] = categorias[i]
        query += ")"
        numresquery += ")"
    # Sección para comprobaciones no join
    if numpars == 0:
        query += " WHERE"
        numresquery += " WHERE"
    else:
        query += " AND"
        numresquery += " AND"
    query += " p.borrado = false AND p.comprador IS NULL AND pe.producto_id = p.id AND p.vendedor=v.id"
    numresquery += " p.borrado = false AND p.comprador IS NULL AND pe.producto_id = p.id AND p.vendedor=v.id"
    # TODO: Pensar bien cómo hacer esta búsqueda, ¿número de apariciones del string?, ¿tiene más peso si aparece en el título?, ...
    if textobusqueda:
        textobusqueda = "%" + textobusqueda + "%"
        query += " AND (p.titulo LIKE :textobusqueda OR p.descripcion LIKE :textobusqueda)"
        numresquery += " AND (p.titulo LIKE :textobusqueda OR p.descripcion LIKE :textobusqueda)"
        query_args['textobusqueda'] = textobusqueda
    if preciomin:
        query += " AND p.\"precioBase\" >= :preciomin"
        numresquery += " AND p.\"precioBase\" >= :preciomin"
        query_args['preciomin'] = preciomin
    if preciomax:
        query += " AND p.\"precioBase\" <= :preciomax"
        numresquery += " AND p.\"precioBase\" <= :preciomax"
        query_args['preciomax'] = preciomax
    if tipocompra:
        query += " AND p.tipo = :tipocompra"
        numresquery += " AND p.tipo = :tipocompra"
        query_args['tipocompra'] = tipocompra
    if latitud:
        query += " AND calcular_distancia(p.latitud, p.longitud, p.radio_ubicacion, :latitud, :longitud, :radio) <= 0"
        numresquery += " AND calcular_distancia(p.latitud, p.longitud, p.radio_ubicacion, :latitud, :longitud, :radio) <= 0"
        query_args['latitud'] = latitud
        query_args['longitud'] = longitud
        query_args['radio'] = radio
    query += " GROUP BY p.id, v.public_id, pe.categoria_nombre LIMIT :number OFFSET :page"
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
        d["multimedia"] = multi
        a.append(d)
    numresquery = "SELECT COUNT(*) FROM (" + query + ") AS res"
    result = db.engine.execute(text(numresquery), query_args)
    for row in result:
        # row.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in row.items():
            # build up the dictionary
            return {
                'resultados': value,
                'productos': a
            }


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
