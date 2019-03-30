from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import ProductoDto
from ..service.producto_service import insertar_producto, get_producto, get_all_products

api = ProductoDto.api
_producto = ProductoDto.producto


@api.route('/')
class ProductoList(Resource):
    @api.doc('lista_de_productos')
    #@admin_token_required
    @api.marshal_list_with(_producto, envelope='data')
    def get(self):
        """List all registered products"""
        return get_all_products()

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
class User(Resource):
    @api.doc('get a producto')
    @api.marshal_with(_producto)
    def get(self, id):
        """get a product given its identifier"""
        producto = get_producto(id)
        if not producto:
            api.abort(404)
        else:
            return producto



