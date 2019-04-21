from app.main.model.usuario import Usuario
from ..service.blacklist_service import save_token


class Auth:

    @staticmethod
    def login_user(data):
        try:
            print(data)
            # fetch the user data
            user_email = Usuario.query.filter_by(email=data.get('email')).first()
            user_nick = Usuario.query.filter_by(nick=data.get('email')).first()
            if user_email:
                user = user_email
            elif user_nick:
                user = user_nick
            if user and user.check_password(data.get('password')):
                if user.validado:
                    auth_token = Usuario.encode_auth_token(user.id)
                    if auth_token:
                        response_object = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'Authorization': auth_token.decode(),
                            'user': user.nick,
                            'public_id': user.public_id
                        }
                        return response_object, 200
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'El usuario no está validado.'
                    }
                    # TODO: REVISAR CÓDIGO ERROR
                    return response_object, 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email/username o contraseña no coinciden.'
                }
                return response_object, 401

        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user(data):
        print(data)
        if data:
            auth_token = data.split(" ")[0]
        else:
            auth_token = ''
        if auth_token:
            resp = Usuario.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                return save_token(token=auth_token)
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403

    @staticmethod
    def get_logged_in_user(new_request):
        # get the auth token
        auth_token = new_request.headers.get('Authorization')
        if auth_token:
            resp = Usuario.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = Usuario.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'user_id': user.id,
                        'email': user.email,
                        # 'admin': user.admin,
                        # 'registered_on': str(user.registered_on)
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 401
