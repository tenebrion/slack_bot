import get_json_data


def return_number_facts():
    """
    This will return a random number and a fact containing that number
    :return: data['number'], data['text']
    """
    # simple url to call
    url = "http://numbersapi.com/random?json"
    data = get_json_data.grab_json_data(url)
    return f"Number: {data['number']}\n" \
           f"Fact: {data['text']}"
