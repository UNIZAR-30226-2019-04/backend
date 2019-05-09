from flask import request
from flask_restplus import Resource

from app.main.util.dto import ValoracionDto
from app.main.util.decorator import admin_token_required
from app.main.service.valoracion_service import save_new_valoracion


api = ValoracionDto.api
_valoracion = ValoracionDto.valoracion


@api.route('/<public_id>')
class Deseados(Resource):
    @api.expect(_valoracion, validate=True)
    @api.response(404, 'Usuario no válido.')
    @api.response(201, 'Valoración realizada.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Añade una valoración a un usuario')
    def post(self, public_id):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return save_new_valoracion(public_id, auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")
