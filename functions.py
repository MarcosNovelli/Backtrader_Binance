from config import client
from binance.enums import *
from typing import List
import datetime as dt
import pandas as pd

'''
        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
'''


def store_ticker_prices_backtest(symbol:str, TF:str, lookback:int=1000) -> pd.DataFrame:
    
    # Devuelve hasta el current candle, con los parametros que tenga en el momento
    klines:list = client.get_historical_klines(symbol, TF, limit=lookback, klines_type=HistoricalKlinesType.FUTURES)
    
    # Create dataframe with all candlestick info
    df = pd.DataFrame(klines)
    
    # Remove unnecesary info
    df = df.iloc[:,0:6]
    
    df.columns = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df["Adj_Close"] = df["Close"]

    df.Open      = df.Open.astype("float")
    df.High      = df.High.astype("float")
    df.Low       = df.Low.astype("float")
    df.Close     = df.Close.astype("float")
    df.Volume    = df.Volume.astype("float")

    df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.Date]

    print(f"Added {symbol} info...")
    
    return df

    
