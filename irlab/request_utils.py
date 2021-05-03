import traceback

import requests
import ujson
from icecream import ic


def send_request(url="", method="GET", params=None):
    if params and not isinstance(params, dict):
        params = ujson.loads(params)

    try:
        byte_response = requests.request(url=url, method=method, data=params, timeout=60)
        parsed_response = ujson.loads(byte_response.content)
        if byte_response.status_code == 200:
            return parsed_response
        else:
            print(parsed_response)
            raise Exception
        # ic(type(json_response))
        return json_response
    except Exception as err:
        print(traceback.format_exc())
