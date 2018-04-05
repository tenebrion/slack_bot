import json
import requests
import remove_chars
from misc import apis

# Setting up initial variables
API_KEY = apis.google()


def return_shorter_url(url):
    """
    This simple method will take a long url and return a short url
    :param url:
    :return:
    """
    # found out that the entries were coming over in this format: <http://www.someurl.com>
    full_url = f"https://www.googleapis.com/urlshortener/v1/url?key={API_KEY}"
    fixed_url = remove_chars.clean_text(url)
    payload = {"longUrl": fixed_url}
    headers = {"content-type": "application/json"}
    # making a post to google API
    r = requests.post(full_url, data=json.dumps(payload), headers=headers).json()
    return f"Short URL: {r['id']}"
