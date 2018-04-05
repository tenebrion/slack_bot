import json
import collections
import get_json_data


def return_stock_prices(quote):
    """
    This function will take a stock symbol, such as aapl and provide the current stock data on it
    :param quote: This is the symbol the user needs to provide
    :return: lots of stock data
    """
    partial_url = "https://api.iextrading.com/1.0/stock/"
    end_url = "/quote"
    full_url = partial_url + quote + end_url
    try:
        r = get_json_data.grab_json_data(full_url)
    except json.decoder.JSONDecodeError:
        return "Please provide a valid stock symbol"

    # Setting this data up in a namedtuple for readability
    Stock_data = collections.namedtuple("Stocks",
                                        "Company "
                                        "Symbol "
                                        "Market_Open_Price "
                                        "Market_Low_Value  "
                                        "Market_High_Value "
                                        "Market_Close_Value "
                                        "Market_Latest_Price")

    company_data = Stock_data(r["companyName"],
                              r["symbol"],
                              r["open"],
                              r["low"],
                              r["high"],
                              r["close"],
                              r["iexRealtimePrice"])

    return f"Stock data for : {company_data[0]} ({company_data[1]})\n" \
           f"Opening Price: {company_data[2]}\n" \
           f"Market Low Price: {company_data[3]}\n" \
           f"Market High Price: {company_data[4]}\n" \
           f"Closing Price: {company_data[5]}\n" \
           f"Latest Price (After hours trading): {company_data[6]}"
