import requests


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
        r = requests.get(url).json()  # converting the json file to the list type
    else:
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key}).json()  # this needs API keys to work

    return r
