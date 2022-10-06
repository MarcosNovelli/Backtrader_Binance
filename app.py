from config import client
from functions import store_ticker_prices_backtest, get_data_since
import backtrader as bt
from teststrategies import SmaCross, SupplyAndDemand, TestStrategy
import datetime as dt


startTime = dt.datetime(2022, 10, 6)
endTime = dt.datetime.now(dt.timezone.utc)


df = get_data_since("BTCUSDT", "1m", startTime, endTime)

# print(store_ticker_prices_backtest("BTCUSDT", "1m", startTime, endTime))


print(df)
cerebro = bt.Cerebro()

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

cerebro.addstrategy(SupplyAndDemand)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
cerebro.run()
cerebro.plot(style="candlestick", fmt_x_data = '%Y-%b-%d %H:%M')