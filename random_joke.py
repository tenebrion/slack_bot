import get_json_data

# URL for random joke
URL = "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke"


def return_joke():
    """
    Simple method to pull a random joke
    :return:
    """
    data = get_json_data.grab_json_data(URL)  # pulling data (json format)
    setup = data["setup"].replace("\\", "")  # stripping out the \ in the data
    punchline = data["punchline"].replace("\\", "")  # stripping out the \ in the data
    return f"{setup}\n" \
           f"{punchline}"
