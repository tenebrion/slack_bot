import json
import requests
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
    payload = {"longUrl": url}  # defining the payload info
    headers = {"content-type": "application/json"}  # defining headers
    r = requests.post(FULL_URL, data=json.dumps(payload), headers=headers).json()  # making a post to google API
    return f"Short URL: {r['id']}"
