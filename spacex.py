import time
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
    flight_nums = []
    launch_dates = []
    rocket_names = []
    first_stages_reused = []
    second_stages_reused = []
    payload_ids = []
    payload_conts = []
    customer = []
    launch_sites = []
    launches = []

    # looping through the json file to grab necessary fields
    for flights in spacex_data:
        flight_nums.append(flights["flight_number"])
        launch_dates.append(flights["launch_date_local"])

        for key, value in flights["rocket"].items():
            if key == "rocket_name":
                rocket_names.append(value)  # e.g. Falcon Heavy

            if key == "first_stage":
                first_stage_data = value

                for value in first_stage_data.values():
                    for things in value:
                        for key, value in things.items():
                            if key == "reused":
                                # This lets us know if the first stage rocket is being reused
                                first_stages_reused.append(value)

            if key == "second_stage":
                second_stage_data = value

                for values in second_stage_data.values():
                    for stuff in values:
                        for key, value in stuff.items():
                            if key == "payload_id":  # this lets us know what they are sending to space
                                payload_ids.append(value)
                            if key == "reused":
                                # This lets us know if the second stage rocket is being reused
                                second_stages_reused.append(value)
                            if key == "payload_type":  # this lets us know what the payload is (e.g. satellite, car)
                                payload_conts.append(value)
                            if key == "customers":  # This lets us know who is paying SpaceX to launch a rocket
                                customer.append(value)

        for key, value in flights["launch_site"].items():
            if key == "site_name_long":  # This lets us know what launch pad is being used
                launch_sites.append(value)

    # time / date info come in ISO 8601 format - 2018-01-07T20:00:00-05:00

    # Currently I am not using this. When I run the program here, I only get a single date & time
    # added to launches. When I run the program separately (line by line), it works fine. Need to
    # troubleshoot it more
    for times in launch_dates:
        try:
            ts = time.strptime(times[:19], "%Y-%m-%dT%H:%M:%S")
            launches.append(time.strftime("%Y-%m-%d @ %H:%M:%S", ts))
        except ValueError:
            continue

        # Not sure if there is a better way to return two sets of launch info.
        # These will go into a slack room chanel and I don't want it horizontally displayed

        """
        This is the additional section for SpaceX launch data. Right now, the API I use
        only has a single upcoming launch data.
           f"Flight Number: {flight_nums[1]}\n" \
           f"Launch Date: {launch_dates[1]}\n" \
           f"Rocket Type: {rocket_names[1]}\n" \
           f"First Stage Rocket Reused: {first_stages_reused[1]}\n" \
           f"Second Stage Rocket Reused: {second_stages_reused[1]}\n" \
           f"Payload: {payload_ids[1]}\n" \
           f"Payload Contents: {payload_conts[1]}\n" \
           f"Customer: {customer[1][0]}\n" \
           f"Launch Site: {launch_sites[1]}"
        """

        return f"Flight Number: {flight_nums[0]}\n" \
               f"Launch Date: {launch_dates[0]}\n" \
               f"Rocket Type: {rocket_names[0]}\n" \
               f"First Stage Rocket Reused: {first_stages_reused[0]}\n" \
               f"Second Stage Rocket Reused: {second_stages_reused[0]}\n" \
               f"Payload: {payload_ids[0]}\n" \
               f"Payload Contents: {payload_conts[0]}\n" \
               f"Customer: {customer[0][0]}\n" \
               f"Launch Site: {launch_sites[0]}\n\n\n" \
