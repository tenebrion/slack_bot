import json
import urllib
from misc import apis
from urllib import request
from urllib.request import urlopen

app_id = apis.oxford_app_id()
app_key = apis.oxford_app_key()
base_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"


def json_formatting(url):
    req = urllib.request.Request(url, headers={'app_id': app_id, 'app_key': app_key})
    with urlopen(req) as response:
        data = response.read()

    encode = response.headers.get_content_charset('utf-8')
    json_prep = data.decode(encode)
    json_format = json_prep.replace("\n", "")
    oxford_data = json.loads(json_format)
    results = oxford_data["results"]
    for stuff in results:
        for crap in stuff["lexicalEntries"]:
            for more_crap in crap["entries"]:
                return more_crap


def define(word):
    word = word.lower()
    URL = base_url + word
    results = json_formatting(URL)
    define_word = []
    for things in results["senses"]:
        define_word.extend(things["definitions"])
    return define_word


def syn_and_ants(word):
    word = word.lower()
    syn_ant = "/synonyms;antonyms"
    url = base_url + word + syn_ant
    results = json_formatting(url)
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
    word = define(user_word)
    word = word[0][0].upper() + word[0][1:]
    new_line = "\n"
    return f"Word: {user_word[0].upper() + user_word[1:].lower()}\n" \
           f"Definition: {word}"


def return_syn_ant(user_word):
    ant, syn = syn_and_ants(user_word)
    return f"Word: {user_word[0].upper() + user_word[1:].lower()}\n" \
           f"Antonyms: {', '.join([x for x in ant])}\n" \
           f"Synonyms: {', '.join([x for x in syn])}"
