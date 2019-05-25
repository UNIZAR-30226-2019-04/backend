import datetime
import threading
from datetime import datetime

from sqlalchemy import text

from app.main.config import mailer
from app.main.model.deseados import Deseados
from app.main.model.producto import Producto
from app.main.model.usuario import Usuario
from app.main.model.pertenece import Pertenece
from app.main.model.multimedia import Multimedia
from app.main.model.categoria import Categoria
from app.main.model.categoriaVisitada import CategoriaVisitada
from app.main.model.puja import Puja
from app.main.service.generar_email import generateEmail_4, generateEmail_5
from .. import db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def insertar_producto(data):
    usuario = Usuario.query.filter_by(public_id=data['vendedor']).first()
    if usuario:
        categoria = Categoria.query.filter_by(nombre=data['categoria']).first()
        if categoria:
            tipo = data['tipo']
            if tipo == 'subasta' and 'fechaexpiracion' not in data:
                response_object = {
                    'status': 'fail',
                    'message': 'La subasta debe tener fecha de expiración.',
                }
                return response_object
            new_producto = Producto(
                precioBase=data['precioBase'],
                descripcion=data['descripcion'],
                titulo=data['titulo'],
                vendedor=usuario.id,
                tipo=tipo
            )
            if 'precioAux' in data:
                new_producto.precioAux=data['precioAux']
            if tipo == 'subasta':
                new_producto.precioAux=new_producto.precioBase
            if 'fechaexpiracion' in data:
                expiracion = data['fechaexpiracion']
                print(expiracion)
                print ('AAAAAAAAAAAAA')
                expiracion2 = datetime.strptime(expiracion, '%d/%m/%Y %H:%M:%S')
                print(expiracion2)
                new_producto.fechaexpiracion = expiracion2
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
            if tipo == 'subasta':
                actual = datetime.now()
                print(expiracion)
                resta = datetime.strptime(expiracion, '%d/%m/%Y %H:%M:%S')-actual
                print(actual)
                print(resta)
                print(resta.total_seconds())
                threading.Timer(resta.total_seconds(), fin_subasta, [new_producto.id]).start()
            response_object = {
                'status': 'success',
                'message': 'Producto creado.',
                'id': new_producto.id,
            }
            return response_object
        else:
            response_object = {
                'status': 'fail',
                'message': 'Categoría no válida.',
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


def get_a_product(id_producto, visitante=None):
    producto = Producto.query.filter_by(id=id_producto, borrado=False).first()

    if producto:
        deseado = False
        categoria = Pertenece.query.filter_by(producto_id=producto.id).first().categoria_nombre
        producto.visualizaciones += 1
        save_changes(producto)
        fechaexpiracion = producto.fechaexpiracion
        if fechaexpiracion is not None:
            fechaexpiracion = fechaexpiracion.strftime("%d/%m/%Y, %H:%M:%S")
        multi = []
        for i in Multimedia.query.filter_by(producto=id_producto).all():
            multi.append({"path": i.path, "tipo": i.tipo})
        if visitante:
            user = Usuario.query.filter_by(public_id=visitante).first()
            if user:
                catvis = CategoriaVisitada.query.filter_by(usuario=user.id, categoria_nombre=categoria).first()
                if catvis:
                    catvis.veces += 1
                else:
                    catvis = CategoriaVisitada(usuario=user.id, categoria_nombre=categoria)
                save_changes(catvis)
                if Deseados.query.filter_by(producto_id=producto.id, usuario_id=user.id).first():
                    deseado = True
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Usuario no encontrado.',
                }
                return response_object, 404
        comprador = None
        if producto.comprador is not None:
            comprador = Usuario.query.filter_by(id=producto.comprador).first().public_id
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
            'comprador': comprador,
            'tipo': producto.tipo,
            'categoria': categoria,
            'multimedia': multi,
            'deseado': deseado,
            'likes': len(Deseados.query.filter_by(producto_id=producto.id).all())
        }
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def search_products(number=None, page=None, textobusqueda=None, preciomin=None, preciomax=None, tipocompra=None,
                    valoracionMin=None, valoracionMax=None, categorias=None, latitud=None, longitud=None, radio=None,
                    usuario=None):
    query_args = {}
    query = "SELECT p.id, p.\"precioBase\", p.\"precioAux\", p.descripcion, p.titulo, p.visualizaciones, p.fecha, " \
            "v.public_id AS vendedor, p.tipo, pe.categoria_nombre, p.latitud, p.longitud, p.radio_ubicacion,"
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
    numpars = 0
    # Sección para joins
    if valoracionMin or valoracionMax:
        query += " WHERE "
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
    query += " p.borrado = false AND p.comprador IS NULL AND pe.producto_id = p.id AND p.vendedor=v.id"
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
    query += " GROUP BY p.id, v.public_id, pe.categoria_nombre"
    numresquery = "SELECT COUNT(*) FROM (" + query + ") AS res"
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
        multi = []
        for i in Multimedia.query.filter_by(producto=d['id']).all():
            multi.append({"path": i.path, "tipo": i.tipo})
        d["multimedia"] = multi
        a.append(d)

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


def fin_subasta(prod_id):
    engine = create_engine('postgresql://jorgegene:jorgegene@localhost:5432/jorgegene')

    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()
    prod = session.query(Producto).filter_by(id=prod_id).first()
    if prod:
        query_args = {}
        query = "SELECT * FROM (SELECT usuario, valor, fecha FROM puja WHERE producto=:id_prod AND valor IN " \
                "(SELECT MAX(valor) FROM puja WHERE producto=:id_prod)) AS g1 WHERE fecha IN (SELECT MIN(fecha) " \
                "FROM (SELECT usuario, valor, fecha FROM puja WHERE producto=:id_prod AND valor IN " \
                "(SELECT MAX(valor) FROM puja WHERE producto=:id_prod)) AS g2)"
        query_args['id_prod'] = prod_id
        result = session.execute(text(query), query_args)
        d, a = {}, []
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                if isinstance(value, datetime):
                    value = value.strftime('%d/%m/%Y')
                d = {**d, **{column: value}}
            a.append(d)
        if a:
            ganador = session.query(Usuario).filter_by(id=a[0]['usuario']).first()
            enviar_mail(prod, ganador, session)
        else:
            enviar_aviso_vendedor(prod, session)
        session.close()


def enviar_mail(prod, ganador, session):
    print("Enviar email")
    try:
        html_email = generateEmail_4(prod, ganador, session)
        mailer.send(
            subject='Has ganado una subasta',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[ganador.email]
        )
        response_object = {
            'status': 'success',
            'message': 'Successfully sent.',
        }
        print(response_object)
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        print(response_object, e)
        return response_object, 401


def enviar_aviso_vendedor(prod, session):
    print("Enviar email")
    try:
        vendedor = session.query(Usuario).filter_by(id=prod.vendedor).first()
        html_email = generateEmail_5(prod, vendedor, session)
        mailer.send(
            subject='Subasta sin pujas',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[vendedor.email]
        )
        response_object = {
            'status': 'success',
            'message': 'Successfully sent.',
        }
        print(response_object)
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        print(response_object, e)
        return response_object, 401


def marcar_venta_realizada(prod_id, comprador, paypal: bool):
    producto = Producto.query.filter_by(id=prod_id, borrado=False).first()
    if producto:
        user = Usuario.query.filter_by(public_id=comprador).first()
        if user:
            producto.comprador = user.id
            producto.paypal = paypal
            save_changes(producto)
            return {'status': 'success'}, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User not found.',
            }
            return response_object, 404
    else:
        response_object = {
            'status': 'fail',
            'message': 'Product not found.',
        }
        return response_object, 404


def save_changes(data):
    db.session.add(data)
    db.session.commit()
