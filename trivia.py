import remove_chars
import get_json_data

# URL for trivia API
URL = "http://jservice.io/api/random"


def return_trivia():
    """
    This connects to an API to pull a random trivia question.
    It is then returned
    :return:
    """
    data = get_json_data.grab_json_data(URL)
    # need to strip out the formatting characters
    answer = remove_chars.clean_text(data[0]["answer"])

    return f"Question: {data[0]['question']}\n" \
           f"Answer: {answer}"
