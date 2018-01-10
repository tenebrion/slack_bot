import re
import get_json_data
from misc import apis
from datetime import datetime
from datetime import timedelta

# Need a API key to get Nasa data
API_KEY = apis.nasa()


def daily_photo(user_date=None):
    """
    This will return the daily nasa photo. It can also return the photo from any selected date
    :param user_date:
    :return:
    """
    planet_url = "https://api.nasa.gov/planetary/apod?"
    planet_date_prep = "date="
    if user_date is None:
        photo_url = planet_url + API_KEY
        nasa_json = get_json_data.grab_json_data(photo_url)
        return nasa_json["hdurl"]
    else:
        photo_url = planet_url + planet_date_prep + user_date + API_KEY
        nasa_json = get_json_data.grab_json_data(photo_url)
        return nasa_json["hdurl"]


def asteroids(start_date, end_date):
    """
    This function will display asteroid info. Right now I'm not using it because there is
    way too much data to present. I'm only using this to post info to slack.
    :param start_date:
    :param end_date:
    :return: asteroid_json
    """
    asteroid_url = "https://api.nasa.gov/neo/rest/v1/feed?"
    asteroid_start_prep = "start_date="
    asteroid_end_prep = "&end_date="
    asteroid_url = asteroid_url + asteroid_start_prep + start_date + asteroid_end_prep + end_date + API_KEY
    asteroid_json = get_json_data.grab_json_data(asteroid_url)
    return asteroid_json["hdurl"]


def nasa(nasa_request):
    """
    this function will return the url for Nasa photos.
    :param nasa_request:
    :return: asteroids
    """
    if "photo" in nasa_request:
        # need to determine if the user wants to specify a date for a past photo
        split_value = nasa_request.split("photo")[1].strip()
        if split_value == "":  # if the user wants the picture from today
            return daily_photo()
        else:  # if the user wants to specify a date in the past for a picture
            return daily_photo(split_value)
    else:
        # this section is under construction. Currently, the asteroid data from Nasa
        # returns 30+ asteroids. This is too much to display in Slack
        match = re.findall(r'\d{4}-\d{2}-\d{2}', nasa_request)
        if len(match) == 0:
            asteroid_start_date = (datetime.now() + timedelta(-30)).strftime("%Y-%m-%d")
            asteroid_end_date = datetime.now().strftime("%Y-%m-%d")
            return asteroids(asteroid_start_date, asteroid_end_date)
        else:
            return asteroids(match[0], match[1])
