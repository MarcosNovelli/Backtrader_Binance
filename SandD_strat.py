import backtrader as bt

class SupplyAndDemand(bt.Strategy):
    '''
    This strategy will replicate a supply and demand scalping
    strategy based on the 1hour timeframe, could possibly work
    on making an adaptable strategy for any timeframe 
    '''
    
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low

        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.trade_type = ''
        self.last_bar_checked = 0

        self.rbd = False
        self.rbr = False
        self.dbr = False
        self.dbd = False

        # Hourly Candles
        self.first_candle_open = -179
        self.first_candle_close = -121
        self.base_open = -119
        self.base_close = -60
        self.third_candle_open = -59
        self.third_candle_close = 0

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Type %s ' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm,
                     self.trade_type))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Type %s' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm,
                          self.trade_type))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f, Type %s' %
                 (trade.pnl, trade.pnlcomm, self.trade_type))

    def check_DBD(self):

        first_low = min(list(self.data.low.get(ago=-120, size=60)))
        second_low = min(list(self.data.low.get(ago=-60, size=60)))
        third_low = min(list(self.data.low.get(ago=-1, size=60)))

        # Detect DBD formation
        Dropbd = self.data.open[self.first_candle_open] > self.data.close[self.first_candle_close] and (self.data.close[self.first_candle_close] - first_low) < (self.data.open[self.first_candle_open] - self.data.close[self.first_candle_close])
        dBased = self.data.close[self.base_close] > self.data.open[self.base_open]
        dbDrop = self.data.open[self.third_candle_open] > self.data.close[self.third_candle_close] and self.data.close[self.third_candle_close] < second_low and (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close]) >= ((self.data.close[self.third_candle_close] - self.data.open[self.base_open]) * 2) and self.data.close[self.third_candle_close] < first_low and (self.data.close[self.third_candle_close] - third_low) < (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close])
        
        DBD = Dropbd and dBased and dbDrop
        
        self.trade_type = "DBD" if DBD else self.trade_type
        
        return DBD
    
    def check_RBD(self):
        
        minus_one_low = min(list(self.data.low.get(ago=-180, size=60)))
        first_low = min(list(self.data.low.get(ago=-120, size=60)))
        basing_low = min( list(self.data.low.get(ago=-60, size=60)))
        third_low = min(list(self.data.low.get(ago=-1, size=60)))
        
        # Detect RBD formation
        Rallybd = self.data.close[self.base_close] > self.data.close[-240]
        print("Drop candle", self.data.open[self.third_candle_open], third_low, self.data.close[self.third_candle_close])
        rBased = self.data.open[self.base_open] < self.data.close[self.base_close]
        rbDrop = self.data.close[self.third_candle_close] < self.data.open[self.third_candle_open] and (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close]) >= ((self.data.close[self.base_close] - self.data.open[self.base_open]) * 1.5) and self.data.close[self.third_candle_close] < basing_low and self.data.close[self.third_candle_close] < first_low and self.data.close[self.third_candle_close] < minus_one_low and (self.data.close[self.third_candle_close] - third_low) * 1.15 < (self.data.open[self.third_candle_open] - self.data.close[self.third_candle_close])
        
        RBD = Rallybd and rBased and rbDrop

        self.trade_type = "RBD" if RBD else self.trade_type

        return RBD
    
    def check_RBR(self):
        return

    def check_DBR(self):
        return

    def next(self):
        # Log the closing price for reference
        self.log('Close, %.2f' % self.dataclose[0])

        if self.order:
            return
        
        # Check if there is an open position
        if not self.position:

            if len(self) > 180:
                # Check if we might like to be in a trade every hour

                if len(self) % 60 == 0:
                    print("CHECKING FOR TRADE")
                    self.dbd = False#self.check_DBD()
                    self.rbd = self.check_RBD()

                    if self.dbd or self.rbd:
                        print("Trade Found")
                        
                        # Order management
                        self.mainside = self.sell(exectype=bt.Order.Market, transmit=False)

                        # self.stop_order = self.buy(price=self.dataclose*1.01, size=self.mainside.size, exectype=bt.Order.Stop,
                        #     transmit=True, parent=self.mainside)

                        self.close_trade = self.buy(exectype=bt.Order.Market, transmit=True, parent=self.mainside)
                        
                        # stop = self.buy(trailpercent=0.05, size=mainside.size, exectype=bt.Order.StopTrail,
                        #     transmit=False, parent=mainside)
                        
                        
                        # Strategy management
                        self.price_executed = self.datas[0].close[0]
                        print(self.price_executed, "PRICE EXECUTED")

                    self.last_bar_checked = len(self) 
        
        # if self.position:
            
        #     if self.dbd and self.stop_order.status != 5:
        #         # Change stop for trailing stop once .05% is reached in profit
        #         if self.datas[0].low <= (self.price_executed * 0.995):
        #             self.cancel(self.stop_order)
        #             trailing_stop = self.buy(price=self.datas[0].low, trailpercent=0.005, size=self.mainside.size, exectype=bt.Order.StopTrail)
        #             print("TRAILING STOP IN PLACE")

            return