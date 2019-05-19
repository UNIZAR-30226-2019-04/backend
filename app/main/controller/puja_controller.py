from flask import request
from flask_restplus import Resource

from app.main.util.dto import PujaDto
from app.main.util.decorator import admin_token_required
from app.main.service.puja_service import save_new_puja, get_pujas


api = PujaDto.api
_puja = PujaDto.puja


@api.route('/')
class Puja(Resource):
    @api.expect(_puja, validate=True)
    @api.response(404, 'Usuario o producto no válidos.')
    @api.response(201, 'Puja creada.')
    @api.response(401, 'Autenticación no válida')
    @api.doc('Crea una puja')
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            data = request.json
            return save_new_puja(auth_header, data=data)
        else:
            api.abort(401, "Se necesita autorización")


@api.route('/<id>')
class Puja(Resource):
    @api.marshal_list_with(_puja, envelope='data')
    @api.response(404, 'Producto no válido.')
    @api.doc('Crea una puja')
    def get(self, id):
        return get_pujas(id)