import time
import json
import weather
import movies
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
    I'll add info later
    :param value:
    :return:
    """
    if "help" in value:
        split_value = value.split("help")[1].strip()
        if split_value == "":
            return "Help Topics: {}".format(", ".join(key for key, value in data["help"].items()))
        else:
            try:
                return data["help"][split_value]
            except KeyError:
                return "I don't have a help file for that command. Adding {} to the backlog".format(value)
    elif "weather" in value:
        split_value = value.split("weather")[1].strip()
        return weather.slack_response(split_value, False)
    elif "movies" in value:
        split_value = value.split("movies")[1].strip()
        return movie_info(split_value)
    else:
        try:
            return data[value]
        except KeyError:
            return "I'll add {} to my list of features to add".format(value)


def movie_info(movie):
    title, release_date, overview = movies.prep_title(movie)
    return "{} ({}): {}".format(title, release_date, overview)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from fire hose
    if slack_client.rtm_connect():
        print("RLSBot is connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            #user_command = topics(command)
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
