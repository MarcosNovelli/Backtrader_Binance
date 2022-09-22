from binance.client import Client
from config import client
from functions import store_ticker_prices_backtest
import yfinance as yf
import backtrader as bt

class SmaCross(bt.Strategy):
    def __init__(self):
        sma1 = bt.ind.SMA(period=50)
        sma2 = bt.ind.SMA(period=100)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        
        elif self.crossover < 0:
            self.close()


cerebro = bt.Cerebro()

store_ticker_prices_backtest([])
df = yf.download("AAPL", start='2020-01-01')
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

cerebro.addstrategy(SmaCross)

cerebro.run()
cerebro.plot()

