from tracemalloc import start
from config import client
from binance.enums import *
from typing import List
import datetime as dt
import pandas as pd
import itertools
import backtrader as bt

'''
        :return: list of OHLCV values (Open time, Open, High, Low, Close, Volume, Close time, Quote asset volume, Number of trades, Taker buy base asset volume, Taker buy quote asset volume, Ignore)
'''

def store_ticker_prices_backtest(symbol:str, TF:str, startTime, endTime=dt.datetime.now().timestamp(), lookback:int=1000) -> pd.DataFrame:

    # Devuelve hasta el current candle, con los parametros que tenga en el momento
    klines:list = client.get_historical_klines(symbol, TF, limit=lookback, start_str=str((startTime + 10800)*1000), end_str=str((endTime + 10800)*1000), klines_type=HistoricalKlinesType.FUTURES)

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

def get_data_since(ticker, TF, startTime, endTime):        
        
        df_list = []
        
        while True:                
                new_df = store_ticker_prices_backtest(ticker, TF, startTime, endTime)
                if new_df is None:
                        break
                
                df_list.append(new_df)
                startTime = max(new_df["Date"]) + 60
                
                if startTime >= endTime:
                        break
        
        all_price_df = pd.concat(df_list)
        all_price_df.to_csv('price_data.csv')
        
        return all_price_df
    
def get_file_data(file:str):
        df = pd.read_csv(file, delimiter=',')
        
        df = df.iloc[:,1:]

        df.columns = ["Date", "Open", "High", "Low", "Close", "Volume", "Adj_Close"]

        df.Open      = df.Open.astype("float")
        df.High      = df.High.astype("float")
        df.Low       = df.Low.astype("float")
        df.Close     = df.Close.astype("float")
        df.Volume    = df.Volume.astype("float")
        df.Adj_Cose  = df.Adj_Close.astype("float")

        df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.Date]

        return df