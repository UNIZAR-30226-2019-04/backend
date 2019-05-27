from flask import request
from flask_restplus import Resource
from app.main.util.dto import DeseadosDto
from app.main.util.decorator import admin_token_required
from app.main.service.deseados_service import save_new_deseado, remove_deseado


api = DeseadosDto.api
_deseados = DeseadosDto.deseados


@api.route('/<public_id>')
class Deseados(Resource):
    @api.expect(_deseados, validate=True)
    @api.response(404, 'Usuario o producto no existen.')
    @api.response(201, 'Producto añadido de la lista.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Añade producto a la lista de deseados')
    def post(self, public_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return save_new_deseado(public_id, auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")


@api.route('/<public_id>/remove')
class Deseados(Resource):
    @api.expect(_deseados, validate=True)
    @api.response(404, 'Usuario o producto no existen.')
    @api.response(201, 'Producto eliminado de la lista.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Quita producto de la lista de deseados')
    def post(self, public_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return remove_deseado(public_id, auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")