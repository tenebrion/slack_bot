import urllib
import json
from misc import apis
from urllib import request
from urllib.request import urlopen

accept = "application/json"
app_id = apis.oxford_app_id()
app_key = apis.oxford_app_key()


def define(word):
    """
    This is where we define our word
    :param word:
    :return:
    """
    base_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"
    region = "/regions=us"
    url = base_url + word + region
    req = urllib.request.Request(url, headers={'app_id': app_id, 'app_key': app_key})
    with urlopen(req) as response:
        data = response.read()

    encoding = response.headers.get_content_charset("utf-8")
    json_prep = data.decode(encoding)
    json_format = json_prep.replace("\n", "")
    oxford_data = json.loads(json_format)
    results = oxford_data["results"]

    # yeah this is crazy. There are lots of nested dictionaries and lists in the json response
    # I also got annoyed drilling that far down. I need to change variable names
    define_word = []
    for stuff in results:
        word_name = stuff["id"]
        for crap in stuff["lexicalEntries"]:
            for more_crap in crap["entries"]:
                for things in more_crap["senses"]:
                    define_word.extend(things["definitions"])
        return word_name, define_word


def return_data(user_word):
    word_1, word_2 = define(user_word)
    word_1 = word_1[0].upper() + word_1[1:]
    word_2 = word_2[0][0].upper() + word_2[0][1:]
    return f"Word: {word_1}\n" \
           f"Definition: {word_2}"
