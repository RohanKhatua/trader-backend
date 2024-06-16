import backtrader as bt

class RSIEntry(bt.SignalStrategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30),)

    def __init__(self):
        rsi = bt.indicators.RSI(self.data.close, period=self.params.period)
        self.signal_add(bt.SIGNAL_LONG, rsi < self.params.oversold)
        self.signal_add(bt.SIGNAL_SHORT, rsi > self.params.overbought)

class RSIExit(bt.SignalStrategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30),)

    def __init__(self):
        rsi = bt.indicators.RSI(self.data.close, period=self.params.period)
        self.signal_add(bt.SIGNAL_LONGEXIT, rsi > self.params.overbought)
        self.signal_add(bt.SIGNAL_SHORTEXIT, rsi < self.params.oversold)
