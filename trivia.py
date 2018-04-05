import remove_chars
import get_json_data


def return_trivia():
    """
    This connects to an API to pull a random trivia question.
    It is then returned
    :return: data[0]['question'], answer
    """
    # URL for trivia API
    url = "http://jservice.io/api/random"
    data = get_json_data.grab_json_data(url)
    # need to strip out the formatting characters
    answer = remove_chars.clean_text(data[0]["answer"])

    return f"Question: {data[0]['question']}\n" \
           f"Answer: {answer}"
