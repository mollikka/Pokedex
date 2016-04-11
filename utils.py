from json import loads as jsonparse
from json import dumps as jsondumps
from cached_query import get_external

def fetch_json(url):
    response = get_external(url)
    data = jsonparse(response)

    return data

def dict_to_json(in_dict):
    return jsondumps(in_dict)
