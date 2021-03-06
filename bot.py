import time
import json
import weather
import movies
import nasa
import xkcd
import bitcoin_prices
import stock_prices
import dictionary
import books
import spacex
import trivia
import google_lat_long
import random_joke
import number_facts
import google_shorten_url
import airplanes_overhead
import chuck_norris_jokes
from misc import apis
from slackclient import SlackClient

# RLS's ID as an environment variable
BOT_ID = apis.rls_bot_name()

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack
slack_client = SlackClient(apis.rls())

# load my json file that contains help contents
# I did this as a learning process
data = json.load(open(r"C:\Users\michael.f.koegel\Documents\GitHub\slack_bot\slack_messages.json"))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = topics(command)
    slack_client.api_call("chat.postMessage",
                          channel=channel,
                          text=response,
                          as_user=True
                          )


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events fire hose.
        This parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def topics(value):
    """
    This method is what calls all the other methods depending on what the user wants.
    :param value:
    :return: topic
    """
    user_topic = value.partition(" ")[0]
    topic_data = value.split(user_topic)[1].strip()

    # Simple dictionary of topics currently available
    available_topics = {
        "spacex": spacex.return_next_launch,
        "syn-ant": dictionary.return_syn_ant,
        "define": dictionary.return_definition,
        "books": books.return_book_details,
        "nasa": nasa.nasa,
        "movies": movies.movie_info,
        "weather": weather.slack_response,
        "xkcd": xkcd.return_xkcd_img,
        "stocks": stock_prices.return_stock_prices,
        "bitcoin": bitcoin_prices.gather_bitcoin_values,
        "lat-long": google_lat_long.return_lat_long,
        "shorten": google_shorten_url.return_shorter_url,
        "airplanes": airplanes_overhead.get_flights_overhead,
        "chuck-norris": chuck_norris_jokes.return_chuck_norris_joke,
        "numbers": number_facts.return_number_facts,
        "joke": random_joke.return_joke,
        "trivia": trivia.return_trivia
    }

    # help topics are pulled from a json file. As such, I treat them differently
    if "help" in user_topic:
        if topic_data == "":
            return f"Help Topics: {', '.join(key for key, value in data['help'].items())}"
        else:
            try:
                return data["help"][topic_data]
            except KeyError:
                return f"I don't have a help file for that command. Adding {user_topic} to the backlog"
    else:
        try:
            # This should return the user topic + add the topic info the user is requesting
            return available_topics[user_topic](topic_data)
        except TypeError:
            # this will call different methods that do not need additional information sent
            return available_topics[user_topic]()
        except KeyError:
            # In the event I don't have a method setup for the user request (or they misspell a topic)
            return f"I'll add {user_topic} to my list of features to add!"


if __name__ == "__main__":
    # 1 second delay between reading from fire hose
    READ_WEBSOCKET_DELAY = 1
    if slack_client.rtm_connect():
        print("RLSBot is connected and running!")
        while True:
            user_command, user_channel = parse_slack_output(slack_client.rtm_read())
            if user_command and user_channel:
                handle_command(user_command, user_channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
