from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductoDto
from ..util.dto import CategoriaListaDto
from ..service.producto_service import insertar_producto, get_product_categories, get_a_product, editar_producto, get_products, add_categorias

api = ProductoDto.api
_producto = ProductoDto.producto
_categorias = CategoriaListaDto.categoriaLista


# TODO Añadir aquí la búsqueda de productos
@api.route('/')
class ProductoList(Resource):
    @api.doc('lista_de_productos')
    #@admin_token_required
    @api.marshal_list_with(_producto, envelope='data')
    def get(self):
        """List all registered products"""
        return get_products()

    @api.expect(_producto, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new producto')
    def post(self):
        """Creates a new producto """
        data = request.json
        return insertar_producto(data=data)


@api.route('/<id>')
@api.param('id', 'The producto identifier')
@api.response(404, 'Producto not found.')
class Product(Resource):
    @api.doc('get a producto')
    @api.marshal_with(_producto)
    def get(self, id):
        """get a product given its identifier"""
        producto = get_a_product(id)
        if not producto:
            api.abort(404)
        else:
            return producto


# TODO: Asegurar que solo el dueño o un administrador puede editar
@api.route('/<id>/edit')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('edit a product')
    @api.expect(_producto, validate=True)
    def post(self, id):
        """edit a product given its identifier"""
        data = request.json
        return editar_producto(id, data=data)


# TODO: Asegurar que solo el dueño o un administrador puede editar
@api.route('/<id>/categorias')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('categorias de un producto')
    # @admin_token_required
    @api.marshal_list_with(_categorias, envelope='data')
    def get(self, id):
        """List all registered categories of given product"""
        return get_product_categories(id)

    @api.doc('add categories to a product')
    @api.expect(_categorias, validate=True)
    def post(self, id):
        """add categories to a product given its identifier"""
        data = request.json
        return add_categorias(id, data=data)

