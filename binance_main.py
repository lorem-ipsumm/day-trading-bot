import config
import sys
import math
from binance.client import Client

# setup client connection
client = Client(config.API_KEY, config.API_SECRET)


# check for proper call structure
def handle_args():
    if len(sys.argv) != 2:
        print("usage: coin [symbol name (ex: BNBBTC)]")
        return sys.exit()

    return True


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


    # get SMA and Bollinger Bands
    sma = calculateSMA()
    bb = calculateBB()



    # print formatted data
    print()
    print(" " + baseAsset + " -> " + quoteAsset + ":")
    print(" Price: " + str(avg_price["price"]))
    print(" 24hr Change: " + str(ticker_change) + "%")
    print(" 24 High: " + str(ticker_high))
    print(" 24 Low: " + str(ticker_low))
    print(" Simple Moving Average (20-days): " + str(sma))
    print("")
    print(" Lower Bollinger Band: " + str(bb[0]))
    print(" Middle Bollinger Band: " + str(bb[1]))
    print(" Upper Bollinger Band: " + str(bb[2]))
    print("")
    print(" https://www.binance.com/en/trade/" + baseAsset + "_" + quoteAsset)

    
# calculate simple moving average (past 20 days)
def calculateSMA():
    # getting data from past 20 days
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
    total = 0
    for kline in klines:
        total += float(kline[4]) # sum of all closing prices of last 20 days
    return (total/20) # returning sma


# calculate Bollinger Bands from simple moving average (SMA)
def calculateBB():
    sma = calculateSMA()
    # getting data from past 20 days
    klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
    total = 0
    for kline in klines:
        sqDeviation = (float(kline[4]) - sma)**2 # calculate squared deviations of each day
        total += sqDeviation # sum of all squared deviations
    deviationValue = math.sqrt((total/20)) # calculate deviation value as a square root of the average deviation from each day
    #actual Bollinger Band calculation
    upperBand = sma + (deviationValue*2)
    middleBand = sma
    lowerBand = sma - (deviationValue*2)
    # Bollinger Bands consists of lower, middle and upper band
    return [lowerBand, middleBand, upperBand]

  
start()

