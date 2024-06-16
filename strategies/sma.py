import backtrader as bt

class SMAEntry(bt.SignalStrategy):
    params = (('short_period', 50), ('long_period', 200),)

    def __init__(self):
        sma1 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        sma2 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        crossover = bt.indicators.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover > 0)
        self.signal_add(bt.SIGNAL_SHORT, crossover < 0)

class SMAExit(bt.SignalStrategy):
    params = (('short_period', 50), ('long_period', 200),)

    def __init__(self):
        sma1 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_period)
        sma2 = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_period)
        crossover = bt.indicators.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONGEXIT, crossover < 0)
        self.signal_add(bt.SIGNAL_SHORTEXIT, crossover > 0)
