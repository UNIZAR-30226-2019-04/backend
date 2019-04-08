from flask import request
from flask_restplus import Resource
import numpy as np

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductoDto
from ..util.dto import CategoriaListaDto
from ..service.producto_service import insertar_producto, get_product_categories, get_a_product, editar_producto, get_products, add_categorias

api = ProductoDto.api
_producto = ProductoDto.producto
_categorias = CategoriaListaDto.categoriaLista


@api.route('/')
class ProductoList(Resource):
    @api.doc('lista_de_productos')
    #@admin_token_required
    @api.marshal_list_with(_producto, envelope='data')
    def get(self):
        """Parámetros opcionales"""
        preciomin = request.args.get('preciomin', default=0, type=float)
        preciomax = request.args.get('preciomax', default=np.inf, type=float)


        """Lista todos los productos registrados"""
        #TODO Pasar parámetros y hacer búsqueda
        return get_products()

    @api.expect(_producto, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new producto')
    def post(self):
        """Crea un nuevo producto"""
        data = request.json
        return insertar_producto(data=data)


@api.route('/<id>')
@api.param('id', 'Identificador del producto.')
@api.response(404, 'Producto no encontrado.')
class Product(Resource):
    @api.doc('Obtiene un producto')
    @api.marshal_with(_producto)
    def get(self, id):
        """Obtiene un producto dado su identificador"""
        producto = get_a_product(id)
        if not producto:
            api.abort(404)
        else:
            return producto


# TODO: Asegurar que solo el dueño o un administrador puede editar
@api.route('/<id>/edit')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Producto no encontrado.')
class Product(Resource):
    @api.doc('Editar un producto')
    @api.expect(_producto, validate=True)
    def post(self, id):
        """Edita un producto dado su identificador"""
        data = request.json
        return editar_producto(id, data=data)


# TODO: Asegurar que solo el dueño o un administrador puede editar
@api.route('/<id>/categorias')
# @api.param('public_id', 'The User identifier')
@api.response(404, 'Producto no encontrado.')
class Product(Resource):
    @api.doc('categorias de un producto')
    # @admin_token_required
    @api.marshal_list_with(_categorias, envelope='data')
    def get(self, id):
        """Lista todas las categorías del producto dado"""
        return get_product_categories(id)

    @api.doc('Añadir categorías a un producto')
    @api.expect(_categorias, validate=True)
    def post(self, id):
        """Añadir categorías a un producto dado su identificador"""
        data = request.json
        return add_categorias(id, data=data)

