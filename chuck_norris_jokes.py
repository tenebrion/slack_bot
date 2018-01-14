import get_json_data

URL = "https://api.chucknorris.io/jokes/random"


def return_chuck_norris_joke():
    """
    Simple method to return a random Chuck Norris joke.
    :return:
    """
    data = get_json_data.grab_json_data(URL)
    return data["value"]
