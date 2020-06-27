import config
import sys
from binance.client import Client

# setup client connection
client = Client(config.API_KEY, config.API_SECRET)


# check for proper call structure
'''
def handle_args():
    if len(sys.argv) != 2:
        print("usage: coin [symbol name (ex: BNBBTC)]")
        return sys.exit()

    return True
'''


# start!
def start():

    # check args
    # handle_args()

    # get the symbol requested
    # symbol = str(sys.argv[1]).upper()

    # set symbol to BTC -> USDT
    symbol = "BTCUSDT"

    # get symbol info from binance
    info = client.get_symbol_info(symbol=symbol)

    # check if symbol is valid
    if (info is None):
        print("invalid symbol")
        sys.exit()

    # get data
    avg_price = client.get_avg_price(symbol=symbol)
    ticker = client.get_ticker(symbol=symbol)
    ticker_change = float(ticker["priceChangePercent"])
    ticker_high = float(ticker["highPrice"])
    ticker_low = float(ticker["lowPrice"])

    baseAsset = info["baseAsset"]
    quoteAsset = info["quoteAsset"]

    # print formatted data
    print()
    print(" " + baseAsset + " -> " + quoteAsset + ":")
    print(" Price: " + str(avg_price["price"]))
    print(" 24hr Change: " + str(ticker_change) + "%")
    print(" 24 High: " + str(ticker_high))
    print(" 24 Low: " + str(ticker_low))
    print(" https://www.binance.com/en/trade/" + baseAsset + "_" + quoteAsset)


start()
