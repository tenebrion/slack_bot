import get_json_data
import collections

# The quantity is changeable based on the limit at the end. I only want top 10
URL = "https://api.coinmarketcap.com/v1/ticker/?limit=10"


def gather_bitcoin_values():
    """
    This is gathering data from the free market API
    :return:
    """
    r = get_json_data.grab_json_data(URL)

    # Setting up variable list
    cryptocurrency_data = []

    count = 0

    # Building namedtuple to quick build the lists of data
    Cryptocurrency = collections.namedtuple("Cryptocurrency", "Name Rank Price Price_1h Price_24h Price_7d")
    while count <= 9:  # this can change based on how many we pull from the URL above
        cryptocurrency_data.append(Cryptocurrency(r[count]["name"],
                                                  r[count]["rank"],
                                                  r[count]["price_usd"],
                                                  r[count]["percent_change_1h"],
                                                  r[count]["percent_change_24h"],
                                                  r[count]["percent_change_7d"]
                                                  )
                                   )
        count += 1

    # yeah yeah. I know I've got a ton of repeated data. I don't know how to get
    # the return method to loop through and return each piece of data.
    return f"{cryptocurrency_data[0]}\n" \
           f"{cryptocurrency_data[1]}\n" \
           f"{cryptocurrency_data[2]}\n" \
           f"{cryptocurrency_data[3]}\n" \
           f"{cryptocurrency_data[4]}\n" \
           f"{cryptocurrency_data[5]}\n" \
           f"{cryptocurrency_data[6]}\n" \
           f"{cryptocurrency_data[7]}\n" \
           f"{cryptocurrency_data[8]}\n" \
           f"{cryptocurrency_data[9]}"
