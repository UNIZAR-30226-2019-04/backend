from flask_restplus import Resource

from ..util.dto import GeocodeDto
from ..service.geocode_service import point_to_address, address_to_point

api = GeocodeDto.api


@api.route('/address/<float:lat>/<float:lon>')
@api.param('lat', 'Latitude')
@api.param('lon', 'Longitude')
class PointToAddress(Resource):
    @api.doc('address')
    def get(self, lat, lon):
        """Gets address given lat,lon"""
        return point_to_address(lat, lon)


@api.route('/point/<string:address>')
@api.param('address', 'Latitude')
class AddressToPoint(Resource):
    @api.doc('point')
    def get(self, address):
        """Gets point given address"""
        return address_to_point(address)
