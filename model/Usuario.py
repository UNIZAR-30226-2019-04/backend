import datetime
import jwt
from model.blacklist import BlacklistToken
from .. import db, flask_bcrypt
from ..config import key
from geoalchemy2 import Geography


class Usuario(db.Model):
    __tablename__ = "Usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), nullable=False, unique=True)
    Nick = db.Column(db.String(20), nullable=False, unique=True)
    Nombre = db.Column(db.String(20), nullable=False)
    Apellidos = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(128), nullable=False)
    Validado = db.Column(db.Boolean, nullable=False, default=False)
    quiereEmails = db.Column(db.Boolean, nullable=False, default=True)
    Valoracion_Media = db.Column(db.Float, nullable=True)
    Ubicacion = db.Column(Geography(geometry_type='POINT', srid=4326), nullable=True)
    Telefono = db.Column(db.Integer, nullable=True)
    Imagen_Perfil_Path = db.Column(db.String(255), nullable=False, default="/default.jpg")
    Borrado = db.Column(db.Borrado, nullable=False, default=False)

    def __repr__(self):
        return "<Usuario '{}'>".format(self.Nick)

    @property
    def password(self):
        raise AttributeError('Password: write-only field')

    @password.setter
    def password(self, password):
        self.Password = flask_bcrypt.generate_password_hash(
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

    def __repr__(self):
        return "<User '{}'>".format(self.username)
