import collections
import get_json_data
import google_lat_long

# http://www.virtualradarserver.co.uk/Documentation/Formats/AircraftList.aspx
# Setting up URL variables
PARTIAL_URL = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat="
LNG_URL = "&lng="
END_URL = "&fDstL=0&fDstU=10"


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
    full_flight_data = []

    # need to call the google method to convert user provide city & state (or country) to Lat & Lng
    latitude, longitude = google_lat_long.return_lat_long(city_state, True)
    full_url = PARTIAL_URL + latitude + LNG_URL + longitude + END_URL  # making our full url
    data = get_json_data.grab_json_data(full_url)  # grabbing the json data
    flight_data = data["acList"]  # this can be a large file and eat memory
    for items in flight_data:
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

    # I can't get this section working. It either prints a single plane entry or crashes (memory constraints)
    """    
    entries = len(call_sign)
    count = 0

    while count < entries:
        count += 1
        return f"Airline: {airline_name[count]}\n" \
               f"Call Sign: {call_sign[count]}\n" \
               f"Plane ID: {flight_id[count]}\n" \
               f"Plane Model: {model[count]}\n" \
               f"Origin: {flight_orig[count]}\n" \
               f"Destination: {flight_dest[count]}\n" \
               f"Country of Origin: {country[count]}\n\n"
    """

    # running this because I can't get the return to iterate through with the returns
    Flights = collections.namedtuple('Flights', "Airline Model Flight_ID Call_Sign Origination Destination Country")

    flight_count = 0  # for the while loop to use
    while flight_count < len(call_sign):
        # calling the named tuple to build a list of lists
        full_flight_data.append(Flights(airline_name[flight_count],
                                        model[flight_count],
                                        flight_id[flight_count],
                                        call_sign[flight_count],
                                        flight_orig[flight_count],
                                        flight_dest[flight_count],
                                        country[flight_count]
                                        )
                                )
        flight_count += 1  # need to increase the count each time it loops through

    return f"{full_flight_data}"
