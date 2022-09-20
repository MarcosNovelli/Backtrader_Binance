from config import client
from binance.enums import *
from typing import List
import json

'''
        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
'''

def store_ticker_prices_backtest(symbols:List):
    
    symbols_dict = dict()


    for symbol in symbols:

        price_history = []

        # Devuelve hasta el current candle, con los parametros que tenga en el momento
        klines = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, "30 day ago UTC", klines_type=HistoricalKlinesType.FUTURES)
        
        for kline in klines:
            kline = kline[:5]
            price_history.append(kline)

        symbols_dict[symbol] = price_history

        print(f"Added {symbol} info...")

    with open("price_list.json", "w") as json_file:
        json.dump(symbols_dict, json_file, indent=4)
        json_file.close()
    
    return

    
