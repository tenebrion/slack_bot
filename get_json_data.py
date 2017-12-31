import json
import urllib
from urllib import request
from urllib.request import urlopen


def grab_json_data(url, need_headers=None, app_id=None, app_key=None):
    """
    This function grabs content from remote APIs and converts it to useful json data
    :param url:
    :param need_headers:
    :param app_id:
    :param app_key:
    :return:
    """
    if need_headers is None:
        req = urllib.request.Request(url)
    else:
        req = urllib.request.Request(url, headers={'app_id': app_id, 'app_key': app_key})

    with urlopen(req) as response:
        data = response.read()

    encode = response.headers.get_content_charset('utf-8')
    json_prep = data.decode(encode)
    json_format = json_prep.replace("\n", "")
    json_data = json.loads(json_format)
    return json_data
