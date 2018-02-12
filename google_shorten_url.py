import json
import requests
import remove_chars
from misc import apis

# Setting up initial variables
API_KEY = apis.google()
FULL_URL = f"https://www.googleapis.com/urlshortener/v1/url?key={API_KEY}"


def return_shorter_url(url):
    """
    This simple method will take a long url and return a short url
    :param url:
    :return:
    """
    # found out that the entries were coming over in this format: <http://www.someurl.com>
    fixed_url = remove_chars.clean_text(url)
    payload = {"longUrl": fixed_url}
    headers = {"content-type": "application/json"}
    # making a post to google API
    r = requests.post(FULL_URL, data=json.dumps(payload), headers=headers).json()
    return f"Short URL: {r['id']}"
