from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.mensaje_controller import api as mensaje_ns
from .main.controller.producto_controller import api as product_ns
from .main.controller.categoria_controller import api as categoria_ns
from .main.controller.categoria_controller import api1 as categoriaL_ns
from .main.controller.geocode_controller import api as geocode_ns
from .main.controller.deseados_controller import api as deseados_ns
from .main.controller.valoracion_controller import api as valoracion_ns
from .main.controller.conversacion_controller import api as conversacion_ns
from .main.controller.multimedia_controller import api as multimedia_ns
from .main.controller.seguir_controller import api as seguir_ns
from .main.controller.reporteUsuario_controller import api as reporteusr_ns
from .main.controller.puja_controller import api as puja_ns


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
api.add_namespace(deseados_ns, path='/deseados')
api.add_namespace(valoracion_ns, path='/valoracion')
api.add_namespace(conversacion_ns, path='/conversacion')
api.add_namespace(multimedia_ns, path='/multimedia')
api.add_namespace(seguir_ns, path='/seguir')
api.add_namespace(reporteusr_ns, path='/report')
api.add_namespace(puja_ns, path='/puja')
