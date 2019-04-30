# -*- coding: utf-8 -*-
from flask import request
from flask_restplus import Resource
from flask import jsonify

from app.main.util.decorator import admin_token_required
from ..util.dto import MensajeDto
from ..service.mensaje_service import save_new_mensaje, get_all_mensajes
from app.main.util.decorator import admin_token_required, token_required


api = MensajeDto.api
_mensaje = MensajeDto.mensaje


@api.route('/<id>')
@api.param('id', 'The Conversation identifier')
@api.response(404, 'Mensaje not found.')
class Mensaje(Resource):
    @api.doc('get a conversation')
    @token_required
    @api.marshal_list_with(_mensaje, envelope='data')
    def get(self, id):
        """get a user conversation given its identifier"""
        mensaje = get_conversation_mensajes(id)
        print(mensaje)
        return mensaje


@api.route('/mensaje/')
class ConversacionList(Resource):

    @api.doc('list_of_messages')
    @admin_token_required
    @token_required
    @api.marshal_list_with(_mensaje, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_messajes()


@api.expect(_mensaje, validate=True)
@api.response(201, 'message successfully created.')
@token_required
@api.doc('create a new conversation')
def post(self):
    """Creates a new User """
    data = request.json
    return save_new_mensaje(data=data)
