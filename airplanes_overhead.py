import get_json_data
import google_lat_long

# http://www.virtualradarserver.co.uk/Documentation/Formats/AircraftList.aspx
# Setting up URL variables
PARTIAL_URL = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat="
LNG_URL = "&lng="
END_URL = "&fDstL=0&fDstU=100"


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
    print(f"{latitude}: {longitude}")
    full_url = PARTIAL_URL + latitude + LNG_URL + longitude + END_URL  # making our full url
    data = get_json_data.grab_json_data(full_url)  # grabbing the json data
    flights = data["acList"]  # this can be a large file and eat memory
    for items in flights:
        for key, value in items.items():
            if key == "From":
                flight_orig.append(value)
            if key == "To":
                flight_dest.append(value)
            if key == "Id":
                flight_id.append(value)
            if key == "Mdl":
                model.append(value)
            if key == "Op":
                airline_name.append(value)
            if key == "Call":
                call_sign.append(value)
            if key == "Cou":
                country.append(value)
    entries = len(call_sign)
    count = -1

    while count < entries:
        count += 1
        return f"Airline: {airline_name[count]}\n" \
               f"Call Sign: {call_sign[count]}\n" \
               f"Plane ID: {flight_id[count]}\n" \
               f"Plane Model: {model[count]}\n" \
               f"Origin: {flight_orig[count]}\n" \
               f"Destination: {flight_dest[count]}\n" \
               f"Country of Origin: {country[count]}\n\n"
