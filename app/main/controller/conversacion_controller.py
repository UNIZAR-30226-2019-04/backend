from flask import request
from flask_restplus import Resource
from flask import jsonify

from app.main.util.decorator import admin_token_required, token_required
from ..util.dto import ConversationDto
from ..service.conversacion_service import save_new_conversation, get_all_conversations, get_a_conversation, get_all_conversations_id

api = ConversationDto.api
_conversacion = ConversationDto.conversacion


@api.route('/')
class ConversacionList(Resource):
    @api.doc('list_of_conversations')
    # @admin_token_required
    @api.marshal_list_with(_conversacion, envelope='data')
    @token_required
    def get(self):
        """List all registered users"""
        return get_all_conversations()

    @api.expect(_conversacion, validate=True)
    @api.response(201, 'conversation successfully created.')
    @token_required
    @api.doc('create a new conversation')
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_conversation(data=data)


@api.route('/all/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'Conversation not found.')
class ConversacionListId(Resource):
    @api.doc('get a conversation')
    @token_required
    @api.marshal_list_with(_conversacion, envelope='data')
    def get(self, id):
        """get a user given its identifier"""
        print(id)
        conversacion = get_all_conversations_id(id)
        print(conversacion)
        return conversacion