import get_json_data

URL = "https://api.coinmarketcap.com/v1/ticker/?limit=5"


def gather_bitcoin_values():
    r = get_json_data.grab_json_data(URL)

    name = []
    rank = []
    price = []
    percent_change_1h = []
    percent_change_24h = []
    percent_change_7d = []

    count = 0

    while count <= 4:
        name.append(r[count]["name"])
        rank.append(r[count]["rank"])
        price.append(r[count]["price_usd"])
        percent_change_1h.append(r[count]["percent_change_1h"])
        percent_change_24h.append(r[count]["percent_change_24h"])
        percent_change_7d.append(r[count]["percent_change_7d"])
        count += 1

    return name, rank, price, percent_change_1h, percent_change_24h, percent_change_7d


def return_bitcoin_data():
    name, rank, price, percent_change_1h, percent_change_24h, percent_change_7d = gather_bitcoin_values()

    count = -1
    while count < 5:
        count += 1
        return f"Name: {name[count]}\n" \
               f"Coin Rank: {rank[count]}\n" \
               f"Current Price: {price[count]}\n" \
               f"1 Hour Change: {percent_change_1h[count]}\n" \
               f"24 Hour Change: {percent_change_24h[count]}\n" \
               f"7 Day Change: {percent_change_7d[count]}"
