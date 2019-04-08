from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.mensaje_controller import api as mensaje_ns
from .main.controller.producto_controller import api as product_ns
from .main.controller.categoria_controller import api as categoria_ns
from .main.controller.categoria_controller import api1 as categoriaL_ns
from .main.controller.geocode_controller import api as geocode_ns


blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='API Telocam',
          version='1.0',
          description='Grupo 4: Margaret Hamilton'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns, path='/user')
api.add_namespace(mensaje_ns, path='/chat')
api.add_namespace(product_ns, path='/producto')
api.add_namespace(categoria_ns, path='/categoria')
api.add_namespace(categoriaL_ns, path='/categoriaL')
api.add_namespace(geocode_ns, path='/geocode')
