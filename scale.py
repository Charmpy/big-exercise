from math import sqrt


def params(up, down, scale, coords, type, centre):
    u_long, u_lat = map(float, up.split())
    d_long, d_lat = map(float, down.split())

    delta = str(sqrt((u_long - d_long) ** 2 + (u_lat - d_lat) ** 2) * scale)
    toponym_longitude, toponym_lattitude = coords.split(" ")
    centre_longitude, centre_lattitude = centre.split(" ")

    map_params = {
        "ll": ",".join([centre_longitude, centre_lattitude]),
        # "spn": ",".join([delta, delta]),
        "l": type,
        "z": str(scale),
        'pt': f'{",".join([toponym_longitude, toponym_lattitude])},ya_ru'
    }
    return map_params
