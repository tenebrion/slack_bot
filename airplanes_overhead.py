import collections
import get_json_data
import google_lat_long

# http://www.virtualradarserver.co.uk/Documentation/Formats/AircraftList.aspx
# Setting up URL variables
PARTIAL_URL = "https://public-api.adsbexchange.com/VirtualRadar/AircraftList.json?lat="
LNG_URL = "&lng="
END_URL = "&fDstL=0&fDstU=100"


def get_flights_overhead(city_state):
    """
    This function will grab the data (json) from get_airplane_data. Once it has this data,
    we extract the useful info and convert it to a namedtuple. This was the easiest way to
    return 50+ flights at a time.
    :param city_state:
    :return:
    """
    # Need to grab flight data
    latitude, longitude = google_lat_long.return_lat_long(city_state, True)
    full_url = PARTIAL_URL + latitude + LNG_URL + longitude + END_URL
    data = get_json_data.grab_json_data(full_url)
    flight_data = data["acList"]

    # Variable list to return lots of flights
    flight_origination = []
    flight_destination = []
    flight_id = []
    model = []
    airline_name = []
    call_sign = []
    country = []
    full_flight_data = []

    for items in flight_data:  # looping though all keys / values in the list
        for key, value in items.items():
            if key == "From":
                flight_origination.append(value)
            if key == "To":
                flight_destination.append(value)
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

    # running this because I can't get the return to iterate through with the returns
    Flights = collections.namedtuple('Flights', "Airline Model Flight_ID Call_Sign Origination Destination Country")

    flight_count = 0  # for the while loop to use
    while flight_count < len(call_sign):
        # calling the named tuple to build a list of lists
        try:
            full_flight_data.append(Flights(airline_name[flight_count],
                                            model[flight_count],
                                            flight_id[flight_count],
                                            call_sign[flight_count],
                                            flight_origination[flight_count],
                                            flight_destination[flight_count],
                                            country[flight_count]
                                            )
                                    )
        except IndexError:  # needed to include this because not all call_sign or flight data is present
            break
        flight_count += 1  # need to increase the count each time it loops through

    if len(call_sign) == 0:
        return "Errors were present. Check out the URL / Code"
    else:
        return f"{full_flight_data}"
