from config import client
from functions import store_ticker_prices_backtest
import backtrader as bt
from teststrategies import SmaCross, SupplyAndDemand, TestStrategy

df = store_ticker_prices_backtest("BTCUSDT", "1m")  
print(df)
cerebro = bt.Cerebro()

feed = bt.feeds.PandasData(dataname=df)
cerebro.adddata(feed)

cerebro.addstrategy(SupplyAndDemand)
cerebro.addsizer(bt.sizers.PercentSizer, percents=50)

cerebro.run()
cerebro.plot(style="candlestick")

#puedo agarrar slices con el get, pero no se que me devuelve, ver bien si puedo agarrar low los con data.low
# cambiar la cantidad a 10 barras