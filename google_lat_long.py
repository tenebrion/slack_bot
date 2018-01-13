import get_json_data
from misc import apis

API_KEY = apis.google()
PARTIAL_URL = "https://maps.googleapis.com/maps/api/geocode/json?&address="
END_URL = "&key="


def return_lat_long(city_state, use_data=None):
    """
    This method is pulling out the latitude and longitude of a city / state (or city / country).
    Depending on how this will be used, it will either return nicely formatted info or it will
    return just the data.
    :param city_state:
    :param use_data:
    :return:
    """
    split_location = city_state.split()
    city = split_location[0]
    state = split_location[1]
    location = city.lower() + "+" + state.lower()  # making sure it's lowercase and space is swapped to +
    full_url = PARTIAL_URL + location + END_URL + API_KEY
    data = get_json_data.grab_json_data(full_url)
    location_data = data["results"][0]["geometry"]["location"]  # makes is easier to work with
    latitude = location_data["lat"]
    longitude = location_data["lng"]
    if use_data is None:  # if we only want the latitude and longitude, this will be the result
        return f"Latitude: {latitude}\n" \
               f"Longitude: {longitude}"
    else:  # if this data will be used in another method call, this data will be the result
        return str(latitude), str(longitude)
