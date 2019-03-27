from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from app.main.config import USER_AGENT
import json

geolocator = Nominatim(user_agent=USER_AGENT)


def point_to_address(lat: float, lon: float):
    try:
        location = geolocator.reverse(str(lat) + ", " + str(lon))
    except GeopyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Error ' + str(e) + ' occurred. Please try again.'
        }
        return response_object, 400
    if location is None:
        response_object = {
            'status': 'fail',
            'message': 'Location not found.'
        }
        return response_object, 404

    return json.dumps(location.raw["address"]), 200


def address_to_point(address: str):
    try:
        location = geolocator.geocode(address, exactly_one=False)
    except GeopyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Error ' + str(e) + ' occurred. Please try again.'
        }
        return response_object, 400
    if location is None:
        response_object = {
            'status': 'fail',
            'message': 'Location not found.'
        }
        return response_object, 404

    response_object = []
    for l in location:
        response_object.append(l.raw)

    return json.dumps(response_object), 200
