import re
import json
from datetime import datetime
from datetime import timedelta
from urllib.request import urlopen
from misc import apis

api_key = apis.nasa()


def daily_photo(user_date):
	"""
    This will return the daily nasa photo. It can also return the photo from any selected date
    :param user_date:
    :return:
	"""
	planet_url = "https://api.nasa.gov/planetary/apod?"
	planet_date_prep = "date="
	if user_date == "photo":
		photo_url = planet_url + api_key
		with urlopen(photo_url) as response:
			data = response.read()

		encoding = response.headers.get_content_charset('utf-8')
		json_prep = data.decode(encoding)
		json_format = json_prep.replace("\n", "")
		nasa_json = json.loads(json_format)
		return nasa_json["hdurl"]
	else:
		photo_url = planet_url + planet_date_prep + user_date + api_key
		with urlopen(photo_url) as response:
			data = response.read()

		encoding = response.headers.get_content_charset('utf-8')
		json_prep = data.decode(encoding)
		json_format = json_prep.replace("\n", "")
		nasa_json = json.loads(json_format)
		return nasa_json["hdurl"]


def asteroids(start_date, end_date):
	asteroid_url = "https://api.nasa.gov/neo/rest/v1/feed?"
	asteroid_start_prep = "start_date="
	asteroid_end_prep = "&end_date="
	asteroid_url = asteroid_url + asteroid_start_prep + start_date + asteroid_end_prep + end_date + api_key
	with urlopen(asteroid_url) as response:
		data = response.read()
	encoding = response.headers.get_content_charset('utf-8')
	json_prep = data.decode(encoding)
	json_format = json_prep.replace("\n", "")
	asteroid_json = json.loads(json_format)
	return asteroid_json["hdurl"]


def nasa(nasa_request):
	if "photo" in nasa_request:
		split_value = nasa_request.split("photo")[1].strip()
		if split_value == "":
			return daily_photo(nasa_request)
		else:
			return daily_photo(split_value)
	else:
		match = re.findall(r'\d{4}-\d{2}-\d{2}', nasa_request)
		if len(match) == 0:
			asteroid_start_date = (datetime.now() + timedelta(-30)).strftime("%Y-%m-%d")
			asteroid_end_date = datetime.now().strftime("%Y-%m-%d")
			return asteroids(asteroid_start_date, asteroid_end_date)
		else:
			return asteroids(match[0], match[1])
