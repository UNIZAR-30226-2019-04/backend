from flask import request
from flask_restplus import Resource

from app.main.util.decorator import admin_token_required
from ..util.dto import CategoriaDto, CategoriaListaDto
from ..service.categoria_service import insertar_categorias, get_all_categorias

api = CategoriaDto.api
_categoria = CategoriaDto.categoria
api1 = CategoriaListaDto.api
_categoriaLista = CategoriaListaDto.categoriaLista


@api.route('/')
class CategoriaList(Resource):
    @api.doc('lista de categorias')
    #@admin_token_required
    @api.marshal_list_with(_categoria, envelope='data')
    def get(self):
        """List all registered categorias"""
        return get_all_categorias()

    @api.expect(_categoriaLista, validate=True)
    @api.response(201, 'Categorias successfully created.')
    @api.doc('create categorias')
    def post(self):
        """Creates new categoria(s) """
        data = request.json
        return insertar_categorias(data=data)