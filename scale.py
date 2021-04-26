from math import sqrt


def params(up, down, scale, coords):
    u_long, u_lat = map(float, up.split())
    d_long, d_lat = map(float, down.split())

    delta = str(sqrt((u_long - d_long) ** 2 + (u_lat - d_lat) ** 2) * scale)
    toponym_longitude, toponym_lattitude = coords.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        # "spn": ",".join([delta, delta]),
        "l": "map",
        "z": str(scale)
    }
    return map_params
