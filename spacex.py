import time
import collections
import get_json_data


def return_next_launch():
    """
    This is a quick a dirty function to print the next SpaceX launch. I don't print / display
    anything more than the next flight. This is because SpaceX doesn't provide it until it locks
    down the info, location, time, etc.
    :return: flight_number, launch date, payload info, flight time
    """
    url = "https://api.spacexdata.com/v2/launches/upcoming"
    # a_url = "https://api.spacexdata.com/v2/launches/upcoming?launch_year=2017"
    spacex_data = get_json_data.grab_json_data(url)

    # setting up our list variables. This is because SpaceX knows about the next ~3 launches,
    # but only provides full details of the next launch.
    flight_numbers = []
    launch_dates = []
    rocket_names = []
    first_stages_reused = []
    second_stages_reused = []
    payload_ids = []
    payload_contents = []
    payload_weight = []
    customer = []
    launch_sites = []
    launch_times = []
    spacex = []

    count = 0

    # This works. Just not sure of the best way to use this. Namedtuples or several lists
    """
    # There has to be a better way. I thought about namedtuples...
    while count < len(spacex_data):
        flight_numbers.append(spacex_data[count]["flight_number"])
        launch_dates.append(spacex_data[count]["launch_date_local"])
        rocket_names.append(spacex_data[count]["rocket"]["rocket_name"])
        first_stages_reused.append(spacex_data[count]["rocket"]["first_stage"]["cores"][0]["reused"])
        second_stages_reused.append(spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["reused"])
        payload_ids.append(spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_id"])
        payload_contents.append(spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_type"])
        # Need to figure out how to handle entries that are blank
        if spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_mass_kg"] is None:
            payload_weight.append("No weight provided")
        else:
            payload_weight.append(spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_mass_kg"])
        customer.append(spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["customers"])
        launch_sites.append(spacex_data[count]["launch_site"]["site_name_long"])
        count += 1
    """

    date_count = 0
    while date_count < len(spacex_data):
        launch_dates.append(spacex_data[date_count]["launch_date_local"])
        date_count += 1

    for times in launch_dates:
        try:
            ts = time.strptime(times[:19], "%Y-%m-%dT%H:%M:%S")
            launch_times.append(time.strftime("%Y-%m-%d @ %H:%M:%S", ts))
        except ValueError:
            continue

    Spacex = collections.namedtuple("SpaceX",
                                    "Flight_Number "
                                    "Launch_Date "
                                    "Rocket_Name "
                                    "First_Stage_Reused "
                                    "Second_Stage_Reused "
                                    "Payload_ID "
                                    "Payload_Type "
                                    "Payload_Weight "
                                    "Customer "
                                    "Launch_Site"
                                    )

    # I'm not sure if this is the best way. I can't alter these tuple values (that I know of).
    # I also don't know how to return multiple entries which is why I went this way.
    while count < len(spacex_data):
        spacex.append(Spacex(spacex_data[count]["flight_number"],
                             launch_times[count],
                             spacex_data[count]["rocket"]["rocket_name"],
                             spacex_data[count]["rocket"]["first_stage"]["cores"][0]["reused"],
                             spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["reused"],
                             spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_id"],
                             spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_type"],
                             spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["payload_mass_kg"],
                             spacex_data[count]["rocket"]["second_stage"]["payloads"][0]["customers"],
                             spacex_data[count]["launch_site"]["site_name_long"]
                             )
                      )
        count += 1
    """
    # time / date info come in ISO 8601 format - 2018-01-07T20:00:00-05:00

    # Currently I am not using this. When I run the program here, I only get a single date & time
    # added to launches. When I run the program separately (line by line), it works fine. Need to
    # troubleshoot it more
    for times in launch_dates:
        try:
            ts = time.strptime(times[:19], "%Y-%m-%dT%H:%M:%S")
            launch_times.append(time.strftime("%Y-%m-%d @ %H:%M:%S", ts))
        except ValueError:
            continue

        # Not sure if there is a better way to return two sets of launch info.
        # These will go into a slack room chanel and I don't want it horizontally displayed
        flight_count = -1  # starting with -1. Not sure how to start with 0 when all I need to do is return data

        # If I don't split this out, when data is returned it crashes the application.
        # Sometimes the API has multiple launches. Other times it only has one.
        # Could I create a function to clean it up?
        if len(flight_numbers) > 1:  # this will return info for two launches if they are present in the API
            while flight_count < 2:
                flight_count += 1  # I don't know if there is around this...
                return f"Flight Number: {flight_numbers[flight_count]}\n" \
                       f"Launch Date: {launch_dates[flight_count]}\n" \
                       f"Rocket Type: {rocket_names[flight_count]}\n" \
                       f"First Stage Rocket Reused: {first_stages_reused[flight_count]}\n" \
                       f"Second Stage Rocket Reused: {second_stages_reused[flight_count]}\n" \
                       f"Payload: {payload_ids[flight_count]}\n" \
                       f"Payload Contents: {payload_contents[flight_count]}\n" \
                       f"Payload Weight: {payload_weight[flight_count]}\n" \
                       f"Customer: {customer[flight_count][0]}\n" \
                       f"Launch Site: {launch_sites[flight_count]}\n\n"
        else:  # This will print if the API only contains one set of launch data
            return f"Flight Number: {flight_numbers[0]}\n" \
                   f"Launch Date: {launch_dates[0]}\n" \
                   f"Rocket Type: {rocket_names[0]}\n" \
                   f"First Stage Rocket Reused: {first_stages_reused[0]}\n" \
                   f"Second Stage Rocket Reused: {second_stages_reused[0]}\n" \
                   f"Payload: {payload_ids[0]}\n" \
                   f"Payload Contents: {payload_contents[0]}\n" \
                   f"Payload Weight: {payload_weight[flight_count]}\n" \
                   f"Customer: {customer[0][0]}\n" \
                   f"Launch Site: {launch_sites[0]}\n\n"
    """
    return f"{spacex[0]}\n" \
           f"{spacex[1]}\n" \
           f"{spacex[2]}\n"
