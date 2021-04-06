import sys
from io import BytesIO
from scale import params
import requests
from PIL import Image


def get_pic_bytes(toponym_to_find):
    # toponym_to_find = '37.50 55.50'

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]

    delta_up = toponym['boundedBy']['Envelope']['upperCorner']
    delta_down = toponym['boundedBy']['Envelope']['lowerCorner']

    map_params = params(delta_up, delta_down, 1, toponym_coodrinates)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    return response.content
