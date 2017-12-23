import time
import json
import urllib
from urllib import request
from urllib.request import urlopen


def return_next_launch():
    """
    This is a quick a dirty function to print the next SpaceX launch. I don't print / display
    anything more than the next flight. This is because SpaceX doesn't provide it until it locks
    down the info, location, time, etc.
    :return: flight_number, launch date, payload info, flight time
    """
    url = "https://api.spacexdata.com/v2/launches/upcoming"
    a_url = "https://api.spacexdata.com/v2/launches/upcoming?launch_year=2017"
    req = urllib.request.Request(url)
    with urlopen(req) as response:
        data = response.read()

    encode = response.headers.get_content_charset('utf-8')
    json_prep = data.decode(encode)
    spacex_data = json.loads(json_prep)
    # setting up our list variables. This is because SpaceX knows about the next ~3 launches,
    # but only provides full details of the next launch.
    flight_nums = []
    launch_dates = []
    rocket_names = []
    first_stages_reused = []
    second_stages_reused = []
    payload_ids = []
    payload_conts = []
    launch_sites = []
    for flights in spacex_data:
        flight_nums.append(flights["flight_number"])
        launch_dates.append(flights["launch_date_utc"])

        for key, value in flights["rocket"].items():
            if key == "rocket_name":
                rocket_names.append(value)
            if key == "first_stage":
                first_stage_data = value
                for value in first_stage_data.values():
                    for things in value:
                        for key, value in things.items():
                            if key == "reused":
                                first_stages_reused.append(value)
            if key == "second_stage":
                second_stage_data = value
                for values in second_stage_data.values():
                    for stuff in values:
                        for key, value in stuff.items():
                            if key == "payload_id":
                                payload_ids.append(value)
                            if key == "reused":
                                second_stages_reused.append(value)
                            if key == "payload_type":
                                payload_conts.append(value)

        for key, value in flights["launch_site"].items():
            if key == "site_name_long":
                launch_sites.append(value)

    # need to loop through the launch dates, update them, and reinsert them
    launches = []
    for times in launch_dates:
        try:
            ts = time.strptime(times[:19], "%Y-%m-%dT%H:%M:%S")
            launches.append(time.strftime("%Y-%m-%d @ %H:%M:%S", ts))
        except ValueError:
            continue

        # I am limiting this to the current upcoming flight. This is because
        # SpaceX doesn't publish a lot of information about flights that aren't 'hard'
        # scheduled. I know everyone wants more than one flight listed, but I don't control it.
        return f"Flight Number: {flight_nums[0]}\n" \
               f"Launch Date: {launches[0]}\n" \
               f"Rocket Type: {rocket_names[0]}\n" \
               f"First Stage Rocket Reused: {first_stages_reused[0]}\n" \
               f"Second Stage Rocket Reused: {second_stages_reused[0]}\n" \
               f"Payload: {payload_ids[0]}\n" \
               f"Payload Contents: {payload_conts[0]}\n" \
               f"Launch Site: {launch_sites[0]}"