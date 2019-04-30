# -*- coding: utf-8 -*-
from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from app.main.config import USER_AGENT

geolocator = Nominatim(user_agent=USER_AGENT)


def point_to_address(lat, lon):
    try:
        location = geolocator.reverse(str(lat) + ", " + str(lon))
    except GeopyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Error ' + str(e) + '. Pruebe otra vez.'
        }
        return response_object, 400
    if location is None:
        response_object = {
            'status': 'fail',
            'message': 'Localización no encontrada.'
        }
        return response_object, 404

    return location.raw["address"], 200


def address_to_point(address):
    try:
        location = geolocator.geocode(address, exactly_one=False)
    except GeopyError as e:
        response_object = {
            'status': 'fail',
            'message': 'Error ' + str(e) + '. Pruebe otra vez.'
        }
        return response_object, 400
    if location is None:
        response_object = {
            'status': 'fail',
            'message': 'Localización no encontrada.'
        }
        return response_object, 404

    response_object = []
    for l in location:
        response_object.append(l.raw)

    return response_object, 200
