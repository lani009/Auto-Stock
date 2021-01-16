from request.dao import Dao
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, GOOG


class BackTester(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 10)
        self.ma2 = self.I(SMA, price, 20)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

if __name__ == "__main__":
    backtest = Backtest(GOOG, BackTester, cash=100000, commission=0.02, exclusive_orders=True)
    backtest.run()
    backtest.plot()
