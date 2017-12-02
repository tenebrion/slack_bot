import os
import time
import json
import weather
from misc import apis
from slackclient import SlackClient

# RLS's ID as an environment variable
BOT_ID = apis.rls_bot_name()

# constants
AT_BOT = "<@" + BOT_ID + ">"

# instantiate Slack
slack_client = SlackClient(apis.rls())


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = command
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
    # TODO: create this data in a DB so that the code is reusable and not ugly - data["help"][0] is useless
    data = json.load(open(r"C:\Users\michael.f.koegel\PycharmProjects\slack_bot\slack_messages.json"))

    if value == "help":
        return "Help Topics: {}, {}, {}, {}".format(data["help"][0],
                                                    data["help"][2],
                                                    data["help"][4],
                                                    data["help"][6])
    elif value == "clear joins" or value == "purge room" or value == "movies":
        return data[value]
    elif value == "weather":
        # weather.user_input(85226)
        return weather.slack_response(int(85226), False)
    elif value == "help weather":
        return data["help"][1]
    elif value == "help purge room":
        return data["help"][3]
    elif value == "help clear joins":
        return data["help"][5]
    elif value == "help movies":
        return data["help"][7]
    else:
        return "I don't have code for that. I'll work on it."


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from fire hose
    if slack_client.rtm_connect():
        print("rlsbot is connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            user_command = topics(command)
            if user_command and channel:
                handle_command(user_command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
