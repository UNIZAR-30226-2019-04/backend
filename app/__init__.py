from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.mensaje_controller import api as mensaje_ns
from .main.controller.geocode_controller import api as geocode_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/user')
api.add_namespace(mensaje_ns, path='/chat')
api.add_namespace(geocode_ns, path='/geocode')
