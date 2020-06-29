import config
import talib
import numpy
from datetime import datetime, timedelta
from binance.client import Client

def start():
    # setup client connection
    client = Client(config.API_KEY, config.API_SECRET)

    # API request historical
    historical_klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
    patternDetection(historical_klines)

    

def patternDetection(historical_klines):
    op = []
    hi = []
    lo = []
    cl = []

    # collecting all open, high, low and close values
    for kline in historical_klines:
        op.append(float(kline[1]))
        hi.append(float(kline[2]))
        lo.append(float(kline[3]))
        cl.append(float(kline[4]))

    # converting lists into (talib-compatible) numpy arrays
    op = numpy.array(op, dtype=float)
    hi = numpy.array(hi, dtype=float)
    lo = numpy.array(lo, dtype=float)
    cl = numpy.array(cl, dtype=float)

    # applying the talib candle functions for pattern recognition on course data 
    candle_names = talib.get_function_groups()['Pattern Recognition']
    for candle in candle_names:
        results = getattr(talib, candle)(op, hi, lo, cl)
        for i in range(len(results)):
            # '0' means that no pattern was found
            if(results[i] != 0):
                dateOfMatch = datetime.today() - timedelta(days=i+1)
                
                # collect data of the match and print it
                print("Pattern: " + candle + " Result: " + str(results[i]) + " - " + str(dateOfMatch))
        

start()