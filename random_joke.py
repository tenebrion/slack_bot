import get_json_data

# URL for random joke
URL = "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke"


def return_joke():
    """
    Simple method to pull a random joke
    :return:
    """
    data = get_json_data.grab_json_data(URL)
    setup = data["setup"].replace("\\", "")
    punchline = data["punchline"].replace("\\", "")
    return f"{setup}\n" \
           f"{punchline}"
