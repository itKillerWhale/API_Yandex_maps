import requests


def get_map(ll, spn, z, name, params):
    map_params = {
        "ll": ll,
        # "spn": spn,
        "l": name,
        "pt": params,
        "size": "450,450",
        "z": z
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return response