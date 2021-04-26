import sys
from io import BytesIO
from scale import params
import requests
from PIL import Image


def get_pic_bytes(toponym_to_find, scale, type, obj, search=False):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if search:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coordinates = toponym["Point"]["pos"]
        centre_coord = toponym["Point"]["pos"]
        toponym_info = toponym['metaDataProperty']['GeocoderMetaData']['text']

    else:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        centre_coord = toponym["Point"]["pos"]
        toponym_coordinates = obj
        toponym_info = ''

    delta_up = toponym['boundedBy']['Envelope']['upperCorner']
    delta_down = toponym['boundedBy']['Envelope']['lowerCorner']

    if not response:
        pass

    map_params = params(
        delta_up, delta_down, scale, toponym_coordinates, type, centre_coord
    )

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return [response.content, toponym_coordinates, centre_coord, toponym_info]
