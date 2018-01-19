import get_json_data

# URL for trivia API
URL = "http://jservice.io/api/random"


def return_trivia():
    """
    This connects to an API to pull a random trivia question.
    It is then returned
    :return:
    """
    # grabbing trivia data (json format)
    data = get_json_data.grab_json_data(URL)
    # need to strip out the formatting characters
    answer = data[0]['answer'].replace("<i>", "").replace("</i>", "")
    return f"Question: {data[0]['question']}\n" \
           f"Answer: {answer}"
