import time
import json
import weather
import movies
import nasa
import xkcd
import dictionary
import books
import spacex
from misc import apis
from slackclient import SlackClient

# RLS's ID as an environment variable
BOT_ID = apis.rls_bot_name()

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack
slack_client = SlackClient(apis.rls())

# load our json file that contains basic commands
data = json.load(open(r"C:\Users\michael.f.koegel\PycharmProjects\slack_bot\slack_messages.json"))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = topics(command)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


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
    This function is what calls all the other functions depending on what the user wants.
    There has to be a better way to accomplish this instead of all the if / elif / else.
    I've tried functions, dictionaries, but I can't get them to initiate function calls
    :param value:
    :return: topic

    I need to fix up this section so it works. I'm on to something that may eliminate the
    nasty if / elif / else
    """
    user_topic = value.partition(" ")[0]
    topic_data = value.split(user_topic)[1].strip()

    # Simple dictionary of topics currently available
    available_topics = {
        "spacex": spacex.return_next_launch,
        "syn-ant": dictionary.return_syn_ant,
        "define": dictionary.return_definition,
        "books": books.book_info,
        "nasa": nasa.nasa,
        "movies": movies.movie_info,
        "weather": weather.slack_response,
        "xkcd": xkcd.return_xkcd_img
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
            # this will return the generic data from the user requested topic
            return available_topics[user_topic]()
        except KeyError:
            # In the event I don't have a method setup for the user request (or they misspell a topic)
            return f"I'll add {user_topic} to my list of features to add!"


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from fire hose
    if slack_client.rtm_connect():
        print("RLSBot is connected and running!")
        while True:
            user_command, user_channel = parse_slack_output(slack_client.rtm_read())
            if user_command and user_channel:
                handle_command(user_command, user_channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
