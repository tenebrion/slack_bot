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
    launch_dates = []
    launch_times = []
    spacex = []

    date_count = 0  # this is to loop through the while loop in our launch_dates list
    while date_count < len(spacex_data):
        launch_dates.append(spacex_data[date_count]["launch_date_local"])
        date_count += 1

    # This will convert our ISO date time format to human readable material (Year-Month-Date @ Hour:Minute:Second)
    # For example, 2018-01-23 @ 13:00:00
    for times in launch_dates:
        try:
            ts = time.strptime(times[:19], "%Y-%m-%dT%H:%M:%S")  # need to use strptime
            launch_times.append(time.strftime("%Y-%m-%d @ %H:%M:%S", ts))  # appending our formatted content to the list
        except ValueError:  # I've only run into this error once and it may have been a fluke, being safe
            continue

    # Creating a namedtuple to store our data. Eventually, I need to learn how to print properly formatted
    # data for the 3 flights listed.
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
    count = 0  # This will help us change the count for the while loop below
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

    # I know this is a cryptic return statement. If I could figure out how to loop through a return statement
    # I'd use something like spacex[0].flight_number so it is easier to read
    return f"{spacex[0]}\n" \
           f"{spacex[1]}\n" \
           f"{spacex[2]}\n"
