import get_json_data

# URL for trivia API
URL = "http://jservice.io/api/random"
bad_chars = ["<i>", "</i>"]


def return_trivia():
    """
    This connects to an API to pull a random trivia question.
    It is then returned
    :return:
    """
    data = get_json_data.grab_json_data(URL)
    # need to strip out the formatting characters
    for char in bad_chars:
        if char in data[0]["answer"]:
            answer = data[0]["answer"].replace(char, "")

    return f"Question: {data[0]['question']}\n" \
           f"Answer: {answer}"
