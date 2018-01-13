import get_json_data
import google_lat_long

# Setting up URL variables
PARTIAL_URL = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat="
LNG_URL = "&lng="
END_URL = "&fDstL=0&fDstU=48.28"


def return_flights_overhead(city_state):
    """
    This will attempt to return all flights currently over any city. It calls a google API query
    to get latitude and longitude to build the url. I currently have the radius set to 30 miles from the
    located provided, but may shrink it. I've seen as many as 150 flights overhead within that zone.
    That would be excessive data to return
    :param city_state:
    :return:
    """
    # Variable list to return lots of flights
    flight_orig = []
    flight_dest = []
    flight_id = []
    model = []
    airline_name = []
    call_sign = []
    country = []

    # need to call the google method to convert user provide city & state (or country) to Lat & Lng
    latitude, longitude = google_lat_long.return_lat_long(city_state, True)
    full_url = PARTIAL_URL + latitude + LNG_URL + longitude + END_URL  # making our full url
    data = get_json_data.grab_json_data(full_url)  # grabbing the json data
    flights = data["acList"]  # this can be a large file and eat memory
    for items in flights:
        for key, value in items.items():
            if key == "From":
                flight_orig.append(value)
            elif key == "To":
                flight_dest.append(value)
            elif key == "Id":
                flight_id.append(value)
            elif key == "Mdl":
                model.append(value)
            elif key == "Op":
                airline_name.append(value)
            elif key == "Call":
                call_sign.append(value)
            elif key == "Cou":
                country.append(value)
            else:
                return "nothing to see here"
    return f"Airline: {airline_name}\n" \
           f"Call Sign: {call_sign}\n" \
           f"Plane ID: {flight_id}\n" \
           f"Plane Model: {model}\n" \
           f"Origin: {flight_orig}\n" \
           f"Destination: {flight_dest}\n" \
           f"Country of Origin: {country}"
