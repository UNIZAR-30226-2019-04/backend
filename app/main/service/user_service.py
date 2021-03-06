import uuid
import threading
import datetime
import random
import time

from app.main import db
from app.main.model.deseados import Deseados
from app.main.model.multimedia import Multimedia
from app.main.model.pertenece import Pertenece
from app.main.model.usuario import Usuario
from app.main.model.producto import Producto
from app.main.model.valoracion import Valoracion
from app.main.service.generar_email import generateEmail, generateEmail_6
from app.main.model.categoriaVisitada import CategoriaVisitada


from ..config import mailer
from sqlalchemy import text, func

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def save_new_user(data):
    user_nick = Usuario.query.filter_by(nick=data['username']).first()
    user_mail = Usuario.query.filter_by(email=data['email']).first()
    if not user_nick and not user_mail:
        new_user = Usuario(
            public_id=str(uuid.uuid4()),
            nick=data['username'],
            email=data['email'],
            password=data['password'],
        )
        save_changes(new_user)
        send_confirmation_email(new_user)
        #threading.Timer(60, recomendar, [new_user.public_id]).start()
        return generate_token(new_user)
    elif user_mail:
        response_object = {
            'status': 'fail',
            'message': 'El email ya está en uso',
        }
        return response_object, 409
    else:
        response_object = {
            'status': 'fail',
            'message': 'El nombre de usuario ya está en uso',
        }
        return response_object, 409


def editar_usuario(public_id, data):
    user = Usuario.query.filter_by(public_id=public_id, borrado=False).first()
    if user:
        if 'nombre' in data:
            user.nombre = data['nombre']
        if 'apellidos' in data:
            user.apellidos = data['apellidos']
        if 'quiereEmails' in data:
            user.quiereEmails = data['quiereEmails']
        if 'telefono' in data:
            user.telefono = data['telefono']
        if 'descripcion' in data:
            user.descripcion = data['descripcion']
        if 'email' in data and user.email != data['email']:
            user_mail = Usuario.query.filter_by(email=data['email']).first()
            if user_mail:
                response_object = {
                    'status': 'fail',
                    'message': 'El email ya está en uso.',
                }
                return response_object, 409
            else:
                user.email = data['email']
        if 'nick' in data and user.nick != data['nick']:
            user_nick = Usuario.query.filter_by(nick=data['nick']).first()
            if user_nick:
                response_object = {
                    'status': 'fail',
                    'message': 'El nombre de usuario ya está en uso.',
                }
                return response_object, 409
            else:
                user.nick = data['nick']
        if 'latitud' in data:
            user.latitud = data['latitud']
            user.longitud = data['longitud']
            user.radio_ubicacion = data['radio_ubicacion']
        if 'Imagen_Perfil_Path' in data:
            user.Imagen_Perfil_Path = data['Imagen_Perfil_Path']
        save_changes(user)
        response_object = {
            'status': 'success',
            'message': 'Usuario editado con éxito.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def get_users():
    return Usuario.query.all()


# Recuperar un usuario dada su id publica
def get_a_user(public_id):
    #recomendar()
    user = Usuario.query.filter_by(public_id=public_id, borrado=False).first()
    if user:
        response_object = {
            'nick': user.nick,
            'descripcion': user.descripcion,
            'nombre': user.nombre,
            'apellidos': user.apellidos,
            'valoracion': user.valoracion_media,
            'imagen_perfil': user.Imagen_Perfil_Path,
            'latitud': user.latitud,
            'longitud': user.longitud,
            'radio_ubicacion': user.radio_ubicacion,
            'valoraciones_hechas': [],
            'valoraciones_recibidas': [],
            'cajas_productos': [],
        }

        id_usr = user.id
        query_args = {}
        # Productos vendidos por el usuario
        query = "SELECT COUNT(*) FROM producto WHERE vendedor = :id AND comprador IS NOT NULL"
        query_args['id'] = id_usr
        result = db.engine.execute(text(query), query_args)
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                response_object['productos_vendidos'] = value

        # Productos comprados por el usuario
        query = "SELECT COUNT(*) FROM producto WHERE comprador = :id"
        result = db.engine.execute(text(query), query_args)
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                response_object['productos_comprados'] = value

        # Productos que el usuario tiene a la venta
        productos = Producto.query.filter_by(vendedor=id_usr).filter_by(comprador=None).all()
        for p in productos:
            deseado = False
            if Deseados.query.filter_by(producto_id=p.id, usuario_id=user.id).first():
                deseado = True
            multi = []
            for i in Multimedia.query.filter_by(producto=p.id).all():
                multi.append({"path": i.path, "tipo": i.tipo})
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'vendedor': user.public_id,
                'tipo': p.tipo,
                'categoria': Pertenece.query.filter_by(producto_id=p.id).first().categoria_nombre,
                'deseado': deseado,
                "multimedia": multi
            }
            response_object['cajas_productos'].append(producto)

        # Productos en la lista de deseados del usuario
        query = "SELECT p.id, p.\"precioBase\", p.\"precioAux\", p.descripcion, p.titulo, p.visualizaciones, " \
                "p.fecha, u.public_id AS vendedor, p.tipo, pe.categoria_nombre AS categoria, true AS deseado " \
                "FROM producto p, deseados d, pertenece pe, usuario u WHERE u.id=p.vendedor " \
                "AND p.id = d.producto_id AND d.usuario_id = :id AND pe.producto_id = p.id AND p.comprador IS NULL"
        result = db.engine.execute(text(query), query_args)
        d, a = {}, []
        for row in result:
            # row.items() returns an array like [(key0, value0), (key1, value1)]
            for column, value in row.items():
                # build up the dictionary
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                d = {**d, **{column: value}}
            multi = []
            for i in Multimedia.query.filter_by(producto=d['id']).all():
                multi.append({"path": i.path, "tipo": i.tipo})
            d["multimedia"] = multi
            a.append(d)
        response_object['deseados'] = a

        # Valoraciones hechas por el usuario
        valoraciones_hechas = Valoracion.query.filter_by(puntuador=id_usr).all()
        for v in valoraciones_hechas:
            usr_puntuado = Usuario.query.filter_by(id=v.puntuado).first()
            valoracion = {
                'titulo': v.titulo,
                'descripcion': v.descripcion,
                'puntuacion': v.puntuacion,
                'puntuador': user.public_id,
                'puntuador_nick': user.nick,
                'puntuador_img': user.Imagen_Perfil_Path,
                'puntuado': usr_puntuado.public_id,
                'puntuado_nick': usr_puntuado.nick
            }
            response_object['valoraciones_hechas'].append(valoracion)

        # Valoraciones recibidas por el usuario
        valoraciones_recibidas = Valoracion.query.filter_by(puntuado=id_usr).all()
        for v in valoraciones_recibidas:
            usr_puntuador = Usuario.query.filter_by(id=v.puntuador).first()
            valoracion = {
                'titulo': v.titulo,
                'descripcion': v.descripcion,
                'puntuacion': v.puntuacion,
                'puntuador': usr_puntuador.public_id,
                'puntuador_nick': usr_puntuador.nick,
                'puntuador_img': usr_puntuador.Imagen_Perfil_Path,
                'puntuado': user.public_id,
                'puntuado_nick': user.nick
            }
            response_object['valoraciones_recibidas'].append(valoracion)
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


# Recuperar la id publica de un usuario dado su nick o email
def get_user_id(nick=None, email=None):
    if nick:
        return Usuario.query.filter_by(nick=nick).first().public_id
    elif email:
        return Usuario.query.filter_by(email=email).first().public_id
    else:
        raise ValueError('Expected either nick or email args')


def get_user_products(public_id, visitante=None):
    usuario = Usuario.query.filter_by(public_id=public_id).first()
    user = None
    print(usuario)
    if usuario:
        response_object = {
            'cajas_productos': [],
        }
        if visitante:
            user = Usuario.query.filter_by(public_id=visitante).first()
            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'Usuario no encontrado.',
                }
                return response_object, 404
        productos = Producto.query.filter_by(vendedor=usuario.id, comprador=None, borrado=False).all()
        for p in productos:
            deseado = False
            multi = []
            for i in Multimedia.query.filter_by(producto=p.id).all():
                multi.append({"path": i.path, "tipo": i.tipo})
            if user:
                if Deseados.query.filter_by(producto_id=p.id, usuario_id=user.id).first():
                        deseado = True
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'latitud': p.latitud,
                'longitud': p.longitud,
                'radio_ubicacion': p.radio_ubicacion,
                'vendedor': Usuario.query.filter_by(id=p.vendedor).first().public_id,
                'tipo': p.tipo,
                'categoria': Pertenece.query.filter_by(producto_id=p.id).first().categoria_nombre,
                'multimedia': multi,
                'deseado': deseado
            }
            response_object['cajas_productos'].append(producto)
        return response_object
    else:
        print("NOUSUARIO")
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def generate_token(user):
    try:
        # generate the auth token
        auth_token = Usuario.encode_auth_token(user.id)
        print(auth_token)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def send_confirmation_email(user):
    print("Enviar email")
    try:
        # generate the auth token
        confirmation_token = Usuario.encode_confirmation_token(user.email)
        html_email = generateEmail(user, confirmation_token)
        mailer.send(
            subject='Bienvenido a Telocam Confirmacion de su correo electronico',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[user.email]
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


def confirm_user_email(public_id, token):
    try:
        user = Usuario.query.filter_by(public_id=public_id).first()
        print(user.email)
        print(type(token))
        print(str(token))
        print(Usuario.decode_confirmation_token(token))
        if user.email == Usuario.decode_confirmation_token(token):
            user.validado = True
            response_object = {
                'status': 'success',
                'message': 'E-mail validado.'
            }
            print(user.nick)
            print(user.email)
            print(user.validado)
            save_changes(user)
            return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def get_comprados(public_id, visitante=None):
    usuario = Usuario.query.filter_by(public_id=public_id).first()
    user = None
    if usuario:
        response_object = {
            'cajas_productos': [],
        }
        if visitante:
            user = Usuario.query.filter_by(public_id=visitante).first()
            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'Usuario no encontrado.',
                }
                return response_object, 404
        productos = Producto.query.filter(Producto.comprador is not None).filter_by(comprador=usuario.id).all()
        for p in productos:
            deseado = False
            if user:
                if Deseados.query.filter_by(producto_id=p.id, usuario_id=user.id).first():
                    deseado = True
            multi = []
            for i in Multimedia.query.filter_by(producto=p.id).all():
                multi.append({"path": i.path, "tipo": i.tipo})
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'vendedor': Usuario.query.filter_by(id=p.vendedor).first().public_id,
                'latitud': p.latitud,
                'longitud': p.longitud,
                'radio_ubicacion': p.radio_ubicacion,
                'tipo': p.tipo,
                'categoria': Pertenece.query.filter_by(producto_id=p.id).first().categoria_nombre,
                'deseado': deseado,
                'multimedia': multi
            }
            response_object['cajas_productos'].append(producto)
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def get_a_user_to_edit(public_id):
    user = Usuario.query.filter_by(public_id=public_id, borrado=False).first()
    response_object = {
            'nick': user.nick,
            'descripcion': user.descripcion,
            'latitud': user.latitud,
            'longitud': user.longitud,
            'radio_ubicacion': user.radio_ubicacion,
            'nombre': user.nombre,
            'apellidos': user.apellidos,
            'mail': user.email,
            'telefono': user.telefono,
            'quiere_mails': user.quiereEmails
        }
    return response_object


def get_vendidos(public_id, visitante=None):
    usuario = Usuario.query.filter_by(public_id=public_id).first()
    user = None
    if usuario:
        response_object = {
            'cajas_productos': [],
        }
        if visitante:
            user = Usuario.query.filter_by(public_id=visitante).first()
            if not user:
                response_object = {
                    'status': 'fail',
                    'message': 'Usuario no encontrado.',
                }
                return response_object, 404
        productos = Producto.query.filter(Producto.comprador != None).filter_by(vendedor=usuario.id).all()
        for p in productos:
            deseado = False
            if user:
                if Deseados.query.filter_by(producto_id=p.id, usuario_id=user.id).first():
                    deseado = True
            multi = []
            for i in Multimedia.query.filter_by(producto=p.id).all():
                multi.append({"path": i.path, "tipo": i.tipo})
            producto = {
                'id': p.id,
                'precioBase': p.precioBase,
                'precioAux': p.precioAux,
                'descripcion': p.descripcion,
                'titulo': p.titulo,
                'visualizaciones': p.visualizaciones,
                'fecha': p.fecha.strftime('%d/%m/%Y'),
                'latitud': p.latitud,
                'longitud': p.longitud,
                'radio_ubicacion': p.radio_ubicacion,
                'vendedor': Usuario.query.filter_by(id=p.vendedor).first().public_id,
                'comprador': Usuario.query.filter_by(id=p.comprador).first().public_id,
                'tipo': p.tipo,
                'categoria': Pertenece.query.filter_by(producto_id=p.id).first().categoria_nombre,
                'deseado': deseado,
                'multimedia': multi
            }
            response_object['cajas_productos'].append(producto)
        return response_object
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def edit_passwd(public_id, auth, data):
    user = Usuario.query.filter_by(public_id=public_id, borrado=False).first()
    if user:
        resp = Usuario.decode_auth_token(auth)
        user_token = Usuario.query.filter_by(id=resp).first()
        if user_token == user:
            if user.check_password(data['oldpassword']):
                user.password = data['password']
                save_changes(user)
                return {'status': 'success', 'message': 'Contraseña cambiada'}, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Contraseña incorrecta.'
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Autorización no válida'
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'El usuario no existe.',
        }
        return response_object, 404


def enviar_mail2(usuario,html_email, session):
    print("Enviar email")
    try:
        mailer.send(
            subject='Recomendaciones telocam',
            html=html_email,
            from_email='telocam.soporte@gmail.com',
            to=[usuario.email]
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


def recomendar():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

    # create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # create a Session
    session = Session()

    print('DENTROOO')
    while(1):
        users = session.query(Usuario).all()
        for user in users:
            quiereEmails = user.quiereEmails
            borrado = user.borrado
            if not borrado and quiereEmails:
                print ('AAAAAAAAAAAAA')
                categoria = session.query(CategoriaVisitada).filter_by(usuario=user.id).order_by(CategoriaVisitada.veces).first()
                if categoria:
                    print('BBBBBB')
                    print (categoria.categoria_nombre)
                    print (categoria.usuario)
                    print (categoria.veces)
                    productos = session.query(Pertenece).filter_by(categoria_nombre=categoria.categoria_nombre).all()
                    if productos:
                        print('CCCCCCCC')
                        producto = random.choice(productos)
                        producto = session.query(Producto).filter_by(id=producto.producto_id).first()
                        vendedor = session.query(Usuario).filter_by(id=producto.vendedor).first()
                        html_email=generateEmail_6(vendedor,producto,user,session)
                        enviar_mail2(user,html_email,session)
        time.sleep(60)
    #session.close()
    #threading.Timer(60, recomendar).start()


def save_token(public_id,data):
    user = Usuario.query.filter_by(public_id=public_id, borrado=False).first()
    if user:
        user.token = data['token']
        save_changes(user)

def delete_user(public_id, auth, data):
    usuario = Usuario.query.filter_by(public_id=public_id).first()
    if usuario:
        resp = Usuario.decode_auth_token(auth)
        user_token = Usuario.query.filter_by(id=resp).first()
        if user_token == usuario:
            if usuario.check_password(data['password']):
                no_vendidos = Producto.query.filter(Producto.comprador is None).filter_by(vendedor=usuario.id).all()
                for prod in no_vendidos:
                    prod.borrado = True
                    if prod.tipo == 'subasta':
                        query_args = {}
                        query = "Select usuario, MAX(fecha) from Puja where producto = :id"
                        query_args['id'] = prod.id
                        puja = db.engine.execute(text(query), query_args)
                        for row in puja:
                            user = Usuario.query.filter_by(id=row[usuario]).first()
                            # TODO: enviar mail de que el objeto que queria se ha borrado porq ya no esta el usuario
                            break
                    save_changes(prod)

                usuario.borrado = True
                save_changes(usuario)
                response_object = {
                    'status': 'success',
                    'message': 'Borrado satisfactorio'
                }
                return response_object, 200


def save_changes(data):
    db.session.add(data)
    db.session.commit()
