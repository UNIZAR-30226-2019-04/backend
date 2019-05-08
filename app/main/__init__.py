from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import logging
from flask_socketio import SocketIO

from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
socketio = SocketIO()


def create_app(config_name):
    app = Flask(__name__)

    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*": {"origins": "*"}},
         allow_headers="*", methods=["GET", "HEAD", "POST", "PUT", "OPTIONS", "DELETE"])

    app.config.from_object(config_by_name[config_name])
    logging.getLogger('flask_cors').level = logging.DEBUG

    db.init_app(app)
    flask_bcrypt.init_app(app)
    socketio.init_app(app)

    return app
