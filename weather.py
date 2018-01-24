from datetime import datetime
import get_json_data
from misc import apis


def weather_url(user_entry, daily_or_weekly):
    """
    Building out the url since this gets repeated a bit
    :param user_entry: This will either be a city name or zip code
    :param daily_or_weekly: This will determine if the user wants a 1 day forecast or 7 days
    :return:
    """
    daily_partial_url = "http://api.openweathermap.org/data/2.5/weather?"
    forecast_partial_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q="
    # The API key is stored in a separate file using tiny db
    api_key = apis.open_weather()
    zip_code_url = "zip="
    city_url = "q="
    number_forecast_days = "&cnt=7"

    if user_entry and not daily_or_weekly:
        return "{}{}{}{}".format(daily_partial_url, zip_code_url, str(user_entry), api_key)
    elif not daily_or_weekly:
        return "{}{}{}{}".format(daily_partial_url, city_url, str(user_entry), api_key)
    else:
        return "{}{}{}{}".format(forecast_partial_url, str(user_entry), number_forecast_days, api_key)


class WeatherConversion:
    """
    building out the blueprint for the weather values.
    """
    def __init__(self, full_url):
        self.full_url = full_url

    def print_weather(self, days):
        """
        This will use all the methods in the class to print out the relevant temperature information
        :param self:
        :param days: either 1 day forecast or a 7-day forecast
        :return:
        """
        if days == 1:
            read_json = get_json_data.grab_json_data(self.full_url)
            location = read_json["name"]
            outside = self.get_outside_outlook(read_json["weather"])
            wind_speed = read_json["wind"]["speed"]
            # wind_direction = self.deg_to_compass(read_json["wind"]["deg"])
            current_temp = self.convert_temp(read_json["main"]["temp"])
            return "Weather for {}:\n" \
                   "Current Temperature: {:.2f}\n" \
                   "Sky: {}\n" \
                   "Wind speed: {} MPH".format(location, current_temp, outside, wind_speed)
        else:
            read_json = get_json_data.grab_json_data(self.full_url)
            outside = read_json["list"]
            """
            Should be:
            for temp in outside:
                stuff = temp["weather"]
                for i in stuff:
                    print(i['description'])

            Each of these will need to be added to a list or a dictionary to print relationally
            """
            return outside

    def get_outside_outlook(self, weather_description):
        """
        Returning the outside weather description (e.g. overcast clouds)
        :return:
        """
        for entries in weather_description:
            return entries["description"]

    def convert_temp(self, temperature):
        """
        Simple kelvin to fahrenheit conversion
        :return:
        """
        return 1.8 * (temperature - 273) + 32

    def deg_to_compass(self, num):
        """
        This will convert wind speed in degrees to the typical 'compass' directions
        :return:
        """
        convert = int((num / 22.5) + .5)
        compass = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                   "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        return compass[(convert % 16)]

    def convert_date_time(self, dt):
        """
        Simple method to convert unix date/time to something more human
        return:
        """
        return datetime.fromtimestamp(dt).strftime("%Y-%m-%d")


def slack_response(user_input, user_want_forecast=False):
    """

    :param user_input:
    :param user_want_forecast:
    :return:
    """
    full_weather_url = weather_url(user_input, user_want_forecast)
    values = WeatherConversion(full_weather_url)
    return values.print_weather(1)
