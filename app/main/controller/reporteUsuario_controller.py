from flask import request
from flask_restplus import Resource
from app.main.util.dto import ReporteUsuarioDto
from app.main.util.decorator import admin_token_required
from app.main.service.reporteUsuario_service import save_new_reporte


api = ReporteUsuarioDto.api
_reporte = ReporteUsuarioDto.reporteusr


@api.route('/')
class Reporte(Resource):
    @api.expect(_reporte, validate=True)
    @api.response(404, 'Usuario no existe.')
    @api.response(201, 'Usuario reportado.')
    @api.doc('Reporta a un usuario')
    def post(self):
        data = request.json
        return save_new_reporte(data=data)
