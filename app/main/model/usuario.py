from .. import db, flask_bcrypt
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key
import datetime
# from geoalchemy2.types import Geometry


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), nullable=False, unique=True)
    nick = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(20), nullable=True)
    apellidos = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    validado = db.Column(db.Boolean, nullable=False, default=False)
    quiereEmails = db.Column(db.Boolean, nullable=False, default=True)
    valoracion_media = db.Column(db.Float, nullable=False, default=0)
    # TODO: Ubicación
    # Ubicacion = db.Column(Geometry(geometry_type='POINT', srid=4326, spatial_index=False), nullable=True)
    # radioUbicacion = db.Column(db.Integer, nullable=False, default=0)
    telefono = db.Column(db.Integer, nullable=True)
    Imagen_Perfil_Path = db.Column(db.String(255), nullable=False, default="/default.jpg")
    borrado = db.Column(db.Boolean, nullable=False, default=False)
    descripcion = db.Column(db.Text, nullable=False, default='')


    @property
    def password(self):
        raise AtributeError('password: write-only field')

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
        return "<Usuario '{}'>".format(self.email)
