from flask_restplus import Resource

from ..util.dto import GeocodeDto
from ..service.geocode_service import point_to_address, address_to_point

api = GeocodeDto.api


@api.route('/address/<float:lat>/<float:lon>')
@api.param('lat', 'Latitud')
@api.param('lon', 'Longitud')
class PointToAddress(Resource):
    @api.response(200, 'OK.')
    @api.response(400, 'Error genérico.')
    @api.response(404, 'Localización no encontrada.')
    @api.doc('address')
    def get(self, lat, lon):
        """Devuelve una dirección dadas latitud y longitud (en sistema de referencia WGS84)."""
        return point_to_address(lat, lon)


@api.route('/point/<string:address>')
@api.param('address', 'Dirección')
class AddressToPoint(Resource):
    @api.doc('point')
    @api.response(200, 'OK.')
    @api.response(400, 'Error genérico.')
    @api.response(404, 'Localización no encontrada.')
    def get(self, address):
        """Devuelve una lista de puntos en sistema de referencia WGS84 dada una dirección."""
        return address_to_point(address)
