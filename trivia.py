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
    return f"Question: {data['question']}\n" \
           f"Answer: {data['answer']}"
