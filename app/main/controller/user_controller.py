import os

from flask import request
from flask_restplus import Resource

from app.main.config import URL_MULTIMEDIA
from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..util.dto import ProductoDto
from ..util.dto import AuthDto
from ..service.user_service import save_new_user, get_a_user, editar_usuario, get_user_products, get_users, \
    confirm_user_email, send_confirmation_email, get_comprados, get_vendidos, get_a_user_to_edit, edit_passwd, \
    delete_user, save_token

api = UserDto.api
_user = UserDto.user
_producto = ProductoDto.producto
user_auth = AuthDto.user_auth
_userReg = UserDto.user_reg
_userDel = UserDto.user_del
_token = UserDto.token


@api.route('/')
class UserList(Resource):
    @api.doc('lista_de_usuarios_registrados')
    #@admin_token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """Lista todos los usuarios registrados"""
        return get_users()

    @api.expect(_userReg, validate=True)
    @api.response(201, 'Usuario creado con éxito.')
    @api.response(409, 'Usuario ya existe.')
    @api.doc('create a new user')
    def post(self):
        """Crea un nuevo Usuario"""
        data = request.json
        return save_new_user(data=data)


@api.route('/<public_id>/edit')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Usuario no encontrado.')
class User2(Resource):
    @api.doc('Obtener un usuario')
    # @api.marshal_with(_user)
    def get(self, public_id):
        """Obtiene un usuario dado su identificador público"""
        user = get_a_user_to_edit(public_id)
        # TODO: Revisar, esto solo pasa si user es None (normalmente tendrá valor, aunque sea el de un error)
        if not user:
            api.abort(404, "Error del servidor")
        else:
            return user


@api.route('/<public_id>')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Usuario no encontrado.')
class User(Resource):
    @api.doc('Obtener un usuario')
    # @api.marshal_with(_user)
    def get(self, public_id):
        """Obtiene un usuario dado su identificador público"""
        user = get_a_user(public_id)
        # TODO: Revisar, esto solo pasa si user es None (normalmente tendrá valor, aunque sea el de un error)
        if not user:
            api.abort(404, "Error del servidor")
        else:
            return user

    # TODO: Asegurar que solo el dueño o un administrador puede editar
    @api.doc('Editar un usuario')
    # TODO: ¿Se esperan todos los campos, algunos con null, o solo los que se van a modificar?
    # @api.expect(_user, validate=True)
    @api.expect(_user)
    # @api.marshal_with(_user)
    @api.response(404, 'Usuario no encontrado.')
    @api.response(201, 'Usuario editado con éxito.')
    def put(self, public_id):
        """Edita un usuario dado su identificador público"""
        data = request.json
        return editar_usuario(public_id, data=data)

    @api.doc('Eliminar un usuario')
    @api.header('Authorization', 'Token')
    @api.expect(_userDel)
    @api.response(201, 'Usuario eliminado.')
    @api.response(401, 'Autenticación no válida')
    def delete(self, public_id):
        """Elimina un usuario dado su identificador público"""
        auth_header = request.headers.get('Authorization')
        data = request.json
        return delete_user(public_id, auth_header, data)


@api.route('/<public_id>/products')
# @api.param('public_id', 'User products')
@api.response(404, 'Usuario no encontrado.')
class UserProducts(Resource):
    @api.doc('Lista de productos del usuario')
    # @api.marshal_with(_producto)
    def get(self, public_id):
        """Obtiene todos los productos de un usuario dado su identificador público"""
        visitante = request.args.get('usuario', default=None, type=str)
        productos = get_user_products(public_id, visitante)
        if productos == 404:
            api.abort(404, "El usuario no existe")
        else:
            return productos


@api.route('/<public_id>/confirmar_email/<token>')
@api.param('public_id', 'ID usuario')
@api.param('token', 'Token de validación')
@api.response(200, 'OK.')
@api.response(401, 'Error genérico.')
@api.response(404, 'No encontrado.')
class UserConfirmEmail(Resource):
    @api.doc('Confirma el email del usuario')
    def get(self, public_id, token):
        """Confirma el e-mail de un usuario dado el token enviado"""
        return confirm_user_email(public_id, token)


# TODO: Asegurar que solo el dueño o un administrador puede
@api.route('/<public_id>/enviar_email_confirmacion')
@api.param('public_id', 'ID usuario')
@api.response(200, 'OK')
@api.response(401, 'Error genérico')
@api.response(404, 'Usuario no encontrado')
@api.response(500, 'Error interno del servidor')
class UserSendConfirmEmail(Resource):
    @api.doc('confirm user email')
    def get(self, public_id):
        """Reenviar el correo de confirmación del e-mail un usuario"""
        return send_confirmation_email(public_id)


@api.route('/<public_id>/vendidos')
class ProductosVendidos(Resource):
    def get(self, public_id):
        visitante = request.args.get('usuario', default=None, type=str)
        return get_vendidos(public_id, visitante)


@api.route('/<public_id>/comprados')
class ProductosVendidos(Resource):
    def get(self, public_id):
        visitante = request.args.get('usuario', default=None, type=str)
        return get_comprados(public_id, visitante)


@api.route('/<public_id>/fotoPerfil/')
class FotoPerfil(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Bad request.')
    def put(self, public_id):
        """Sube la imagen de perfil del usuario"""

        UPLOAD_FOLDER = '/var/www/html/user/'
        # UPLOAD_FOLDER = '/srv/http/'
        SERVER_ROUTE = URL_MULTIMEDIA + '/user/'
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

        # check if the post request has the file part
        if 'file' not in request.files:
            return ({'status': 'fail', 'error': 'no file'}), 400

        # check if user exists
        user = get_a_user(public_id)
        if user:
            file = request.files['file']
            if file and '.' in file.filename:
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                if file_extension in ALLOWED_EXTENSIONS:
                    file_path = str(public_id + '.' + file_extension)
                    file.save(os.path.join(UPLOAD_FOLDER, file_path))
                    editar_usuario(public_id, data={'Imagen_Perfil_Path': SERVER_ROUTE + file_path})
                    return ({'status': 'success', 'message': 'Archivo subido correctamente',
                             "data": [{"path": SERVER_ROUTE + file_path}]}), 200
                return ({'status': 'fail', 'error': 'extension not allowed'}), 400
            return ({'status': 'fail', 'error': 'file not allowed'}), 400
        return ({'status': 'fail', 'error': 'user not found'}), 400


@api.route('/<public_id>/editpasswd')
@api.header('Authorization', 'Token')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Usuario no encontrado.')
class UserP(Resource):
    @api.doc('Obtener un usuario')
    @api.response(201, 'Contraseña cambiada.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Cambia la contraseña de un usuario')
    def post(self, public_id):
        """Obtiene un usuario dado su identificador público"""
        auth_header = request.headers.get('Authorization')
        data = request.json
        return edit_passwd(public_id, auth_header, data=data)

@api.route('/<public_id>/token/')
@api.expect(_token)
@api.response(200, 'Token guardado con exito')
class SaveNotificationToken(Resource):
    @api.doc('Funcion guardar token')
    @api.marshal_list_with(_token,envelope='data')
    def post(self,public_id):
        data = request.json
        return save_token(public_id, data=data)
