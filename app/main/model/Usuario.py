from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key


class Usuario(db.Model):
    __tablename__ = "Usuario"

    id = db.Column(db.Integer, primary_key=False, autoincrement=True)
    Nick = db.Column(db.String(255), primary_key=True)
    Nombre = db.Column(db.String(255), nullable=False)
    Apellidos = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    Validado = db.Column(db.Boolean, nullable=False, default=False)
    quiereEmails = db.Column(db.Boolean, nullable=False, default=True)
    Valoracion_Media = db.Column(db.Float, nullable=False, default=0.0)
    Ubicacion = db.Column(db.Float, nullable=True)
    Telefono = db.Column(db.Integer, nullable=True)



    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def encode_confirmation_token(user_mail):
        """
        Generates the Confirmation Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_mail
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_confirmation_token(confirmation_token):
        """
        Decodes the confirmation token
        :param confirmation_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(confirmation_token, key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired.'
        except jwt.InvalidTokenError:
            return 'Invalid token.'

    def __repr__(self):
        return "<Usuario '{}'>".format(self.Nick)
