import json
import get_json_data

PARTIAL_URL = "https://api.iextrading.com/1.0/stock/"
END_URL = "/quote"


def return_stock_prices(quote):
    full_url = PARTIAL_URL + quote + END_URL
    try:
        r = get_json_data.grab_json_data(full_url)
    except json.decoder.JSONDecodeError:
        return "Please provide a valid stock sybol"

    market_symbol = r["symbol"]
    company_name = r["companyName"]
    market_close_value = r["close"]
    market_high_value = r["high"]
    market_low_value = r["low"]
    market_open_price = r["open"]
    market_latest_price = r["iexRealtimePrice"]

    return f"Stock data for : {company_name} ({market_symbol})\n" \
           f"Opening Price: {market_open_price}\n" \
           f"Market Low Price: {market_low_value}\n" \
           f"Market High Price: {market_high_value}\n" \
           f"Closing Price: {market_close_value}\n" \
           f"Latest Price (After hours trading): {market_latest_price}"