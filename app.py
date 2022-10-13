from config import client
from functions import get_data_since, get_file_data
import backtrader as bt
from teststrategies import SmaCross, SupplyAndDemand, TestStrategy
import datetime as dt
import pandas as pd

# Choose to download(1) or already downloaded data(0)
download = 1

# Both in seconds
startTime = (dt.datetime(2021, 10, 13)).timestamp()
# endTime = (dt.datetime(2022, 10, 9)).timestamp()
endTime = dt.datetime.now().timestamp()

df = get_data_since("BTCUSDT", "1m", startTime, endTime) if download else get_file_data('price_data.csv')

print(df)
cerebro = bt.Cerebro()

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

cerebro.addstrategy(SupplyAndDemand)
cerebro.broker.setcash(1000)
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
cerebro.run()
cerebro.plot(style="candlestick", fmt_x_data = '%Y-%b-%d %H:%M')