from flask import request
from flask_restplus import Resource
from app.main.util.dto import SeguirDto
from app.main.util.decorator import admin_token_required
from app.main.service.seguir_service import save_new_seguir, dejar_seguir


api = SeguirDto.api
_seguir = SeguirDto.seguir


@api.route('/<public_id>')
class Deseados(Resource):
    @api.expect(_seguir, validate=True)
    @api.response(404, 'Usuario no existe.')
    @api.response(201, 'Usuario seguido.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Añade usuario a la lista de seguidos')
    def post(self, public_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return save_new_seguir(public_id, auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")


@api.route('/<public_id>/remove')
class Deseados(Resource):
    @api.expect(_seguir, validate=True)
    @api.response(404, 'Usuario no existe.')
    @api.response(201, 'Usuario eliminado de la lista de seguidos.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Quita usuario de la lista de seguidos')
    def post(self, public_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return dejar_seguir(public_id, auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")