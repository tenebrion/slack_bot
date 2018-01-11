import get_json_data

URL = "https://api.coinmarketcap.com/v1/ticker/?limit=5"


def gather_bitcoin_values():
    """
    This is gathering data from the free market API
    :return:
    """
    r = get_json_data.grab_json_data(URL)

    # Setting up variable lists
    name = []
    rank = []
    price = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []

    count = 0
    return_count = -1

    while count <= 4:  # looping through values to collect
        name.append(r[count]["name"])
        rank.append(r[count]["rank"])
        price.append(r[count]["price_usd"])
        percent_change_1h.append(r[count]["percent_change_1h"])
        percent_change_24h.append(r[count]["percent_change_24h"])
        percent_change_7d.append(r[count]["percent_change_7d"])
        count += 1

    while return_count < 4:
        return_count += 1
        return f"Name: {name[return_count]}\n" \
               f"Coin Rank: {rank[return_count]}\n" \
               f"Current Price: {price[return_count]}\n" \
               f"1 Hour Change: {percent_change_1h[return_count]}\n" \
               f"24 Hour Change: {percent_change_24h[return_count]}\n" \
               f"7 Day Change: {percent_change_7d[return_count]}\n\n"
