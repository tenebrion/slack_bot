import get_json_data

# simple url to call
URL = "http://numbersapi.com/random?json"


def return_number_facts():
    """
    This will return a random number and a fact containing that number
    :return:
    """
    data = get_json_data.grab_json_data(URL)
    return f"Number: {data['number']}\n" \
           f"Fact: {data['text']}"
