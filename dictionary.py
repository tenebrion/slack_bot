import json
import urllib
from misc import apis
from urllib import request
from urllib.request import urlopen

# setting up our initial variables for the API info
app_id = apis.oxford_app_id()
app_key = apis.oxford_app_key()
base_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"


def json_formatting(url):
    """
    This function will prep the URL for consumption into a json format. This will
    allow us to treat the data like a dictionary and iterate through it
    :param url:
    :return: additional_values
    """
    req = urllib.request.Request(url, headers={'app_id': app_id, 'app_key': app_key})
    with urlopen(req) as response:
        data = response.read()

    encode = response.headers.get_content_charset('utf-8')
    json_prep = data.decode(encode)
    json_format = json_prep.replace("\n", "")
    oxford_data = json.loads(json_format)
    results = oxford_data["results"]
    for stuff in results:
        for values in stuff["lexicalEntries"]:
            for additional_values in values["entries"]:
                return additional_values


def define(word):
    """
    This function will return the definition of a word.
    :param word:
    :return: define_word
    """
    word = word.lower()
    URL = base_url + word
    results = json_formatting(URL)
    define_word = []
    for things in results["senses"]:
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
    results = json_formatting(url)
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
    word = word[0][0].upper() + word[0][1:]
    new_line = "\n"
    return f"Word: {user_word[0].upper() + user_word[1:].lower()}\n" \
           f"Definition: {word}"


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
