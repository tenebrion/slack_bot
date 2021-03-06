import get_json_data
from misc import apis
import google_lat_long
from datetime import datetime


def weather_url(user_entry, city=None):
    """
    This will return the URL to use.
    :param user_entry:
    :param city:
    :return:
    """
    daily_partial_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = apis.open_weather()
    zip_code_url = "zip="
    # Using latitude + longitude is more accurate than using 'city / state (country)
    latitude, longitude = google_lat_long.return_lat_long(user_entry, True)
    lat_url = "lat="
    lon_url = "&lon="

    if city is None:
        return f"{daily_partial_url}{zip_code_url}{str(user_entry)}{api_key}"
    else:
        return f"{daily_partial_url}{lat_url}{latitude}{lon_url}{longitude}{api_key}"


def convert_temp(temperature):
    """
    Simple kelvin to fahrenheit conversion
    :return:
    """
    return 1.8 * (temperature - 273) + 32


def deg_to_compass(num):
    """
    This will convert wind speed in degrees to the typical 'compass' directions
    :return:
    """
    convert = int((num / 22.5) + .5)
    compass = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
               "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return compass[(convert % 16)]


def convert_time(date_time):
    """
    Simple method to convert unix date/time to human format
    This is specific to the sunrise / sunset
    """
    return datetime.fromtimestamp(date_time).strftime("%H:%M:%S")


def grab_weather_data(content):
    """
    This will convert the content from the json file to the
    contents we care about.
    :param content:
    :return:
    """
    # Wonder if it's better to build this as a named tuple...
    temperature = convert_temp(content["main"]["temp"])
    weather_description = content["weather"][0]["description"]
    humidity = content["main"]["humidity"]
    wind_speed = content["wind"]["speed"]
    wind_degrees = deg_to_compass(content["wind"]["deg"])
    location = content["name"]
    sunrise = convert_time(content["sys"]["sunrise"])
    sunset = convert_time(content["sys"]["sunset"])
    deg_symbol = u"\xb0"

    return f"Weather conditions for {location}:\n" \
           f"Temperature: {temperature}{deg_symbol}F\n" \
           f"Current View: {weather_description}\n" \
           f"Humidity: {humidity}%\n" \
           f"Wind Speed: {wind_speed} MPH\n" \
           f"Wind Direction: {wind_degrees}\n" \
           f"Sunrise: {sunrise} AM\n" \
           f"Sunset: {sunset} PM"


def slack_response(user_input):
    """
    This method will return our contents to our slack channel
    :param user_input:
    :return:
    """
    try:
        user_zip_code = int(user_input)
        full_weather_url = weather_url(user_zip_code)
    except ValueError:
        full_weather_url = weather_url(user_input, True)

    # Not sure why I set this here instead in the 'grab weather data function
    values = get_json_data.grab_json_data(full_weather_url)
    return grab_weather_data(values)
