from config import client
from functions import store_ticker_prices_backtest, get_data_since
import backtrader as bt
from teststrategies import SmaCross, SupplyAndDemand, TestStrategy
import datetime as dt

# Both in seconds
startTime = (dt.datetime(2022, 9, 6)).timestamp()
endTime = dt.datetime.now().timestamp()

df = get_data_since("BTCUSDT", "1m", startTime, endTime)

# df = store_ticker_prices_backtest("BTCUSDT", "1m", 1665092760000, endTime)



print(df)
# cerebro = bt.Cerebro()

# feed = bt.feeds.PandasData(dataname=df)
# cerebro.adddata(feed)

# cerebro.addstrategy(SupplyAndDemand)
# cerebro.addsizer(bt.sizers.PercentSizer, percents=50)
# cerebro.run()
# cerebro.plot(style="candlestick", fmt_x_data = '%Y-%b-%d %H:%M')