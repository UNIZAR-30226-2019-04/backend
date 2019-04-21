from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from flask_cors import CORS, cross_origin


api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
# Send Access-Control-Allow-Headers
class UserLogin(Resource):
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    @api.response(401, 'Contraseña o email o username incorrectos')
    def post(self):
        """Recurso de login Usuario"""
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
# Send Access-Control-Allow-Headers
class LogoutAPI(Resource):
    @api.doc('logout a user')
    @api.response(403, 'Token invalido.')
    def post(self):
        """Recurso de logout Usuario"""
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)
