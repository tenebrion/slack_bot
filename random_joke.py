import remove_chars
import get_json_data


def return_joke():
    """
    Simple method to pull a random joke
    :return: setup, punchline
    """
    # URL for random joke
    url = "https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke"
    data = get_json_data.grab_json_data(url)  # pulling data (json format)
    setup = remove_chars.clean_text(data["setup"])
    punchline = remove_chars.clean_text(data["punchline"])
    return f"{setup}\n" \
           f"{punchline}"
