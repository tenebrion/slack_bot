import get_json_data
from misc import apis

# setting up our initial variables for the API info
app_id = apis.oxford_app_id()
app_key = apis.oxford_app_key()
base_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"


def define(word):
    """
    This function will return the definition of a word.
    :param word:
    :return: define_word
    """
    word = word.lower()
    url = base_url + word
    results = get_json_data.grab_json_data(url, True, app_id, app_key)
    define_word = []
    get_def = results["results"][0]["lexicalEntries"][0]["entries"][0]["senses"]
    for things in get_def:
        define_word.extend(things["definitions"])
    return define_word


def syn_and_ants(word):
    """
    This function will take in the word and return the synonyms and antonyms of the word
    :param word:
    :return: ant_words, syn_words
    """
    word = word.lower()
    syn_ant = "/synonyms;antonyms"
    url = base_url + word + syn_ant
    results = get_json_data.grab_json_data(url, True, app_id, app_key)
    results = results["results"]
    # we need to toss these into a list since there are multiple entries
    ant_words = []
    syn_words = []
    for things in results["senses"]:
        syn_ant_data = things
        for ants in syn_ant_data["antonyms"]:
            for key, value in ants.items():
                if key == "id":
                    ant_words.append(value)

            for syns in syn_ant_data["synonyms"]:
                for key, value in syns.items():
                    if key == "id":
                        syn_words.append(value)
    return ant_words, syn_words


def return_definition(user_word):
    """
    This function will return the user word and definition of the word
    :param user_word:
    :return: user_word, word
    """
    word = define(user_word)
    new_line = "\n"
    return f"Word: {user_word[0].upper() + user_word[1:].lower()}\n" \
           f"Definition: {new_line.join([x for x in word])}"


def return_syn_ant(user_word):
    """
    This function takes the word and gets the synonym and antonym. It formats it into
    a nicer message to display
    :param user_word:
    :return: user_word, ant, syn
    """
    ant, syn = syn_and_ants(user_word)
    return f"Word: {user_word[0].upper() + user_word[1:].lower()}\n" \
           f"Antonyms: {', '.join([x for x in ant])}\n" \
           f"Synonyms: {', '.join([x for x in syn])}"
