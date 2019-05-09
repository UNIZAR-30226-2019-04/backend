from flask import request
from flask_restplus import Resource
from app.main.util.decorator import admin_token_required
from ..util.dto import UserDto
from ..util.dto import ProductoDto
from ..util.dto import AuthDto
from ..service.user_service import save_new_user, get_a_user, editar_usuario, get_user_products, get_users, \
    confirm_user_email, send_confirmation_email, get_comprados, get_vendidos

api = UserDto.api
_user = UserDto.user
_producto = ProductoDto.producto
user_auth = AuthDto.user_auth
_userReg = UserDto.user_reg


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


@api.route('/<public_id>/products')
# @api.param('public_id', 'User products')
@api.response(404, 'Usuario no encontrado.')
class UserProducts(Resource):
    @api.doc('Lista de productos del usuario')
    # @api.marshal_with(_producto)
    def get(self, public_id):
        """Obtiene todos los productos de un usuario dado su identificador público"""
        productos = get_user_products(public_id)
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
        user = get_a_user(public_id)
        return send_confirmation_email(user)


@api.route('/<public_id>/vendidos')
class ProductosVendidos(Resource):
    def get(self, public_id):
        return get_vendidos(public_id)


@api.route('/<public_id>/comprados')
class ProductosVendidos(Resource):
    def get(self, public_id):
        return get_comprados(public_id)
