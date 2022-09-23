from binance.client import Client
from config import client
from functions import store_ticker_prices_backtest
import yfinance as yf
import backtrader as bt
from teststrategies import SmaCross, TestStrategy

df = store_ticker_prices_backtest("BTCUSDT", "1h")
print(df)



cerebro = bt.Cerebro()

# feed = yf.download("AAPL", start='2020-01-01')
# print(feed)
feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

# cerebro.addstrategy(TestStrategy)
# cerebro.broker.setcommission(commission=0.005)
# cerebro.addsizer(bt.sizers.PercentSizer, percents=50)

cerebro.run()
cerebro.plot(style="candlestick")
