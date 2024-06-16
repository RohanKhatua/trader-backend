import yfinance as yf
import backtrader as bt
import pandas as pd

def load_data(data_source, symbol, start_date, end_date):
    if data_source == 'yahoo':
        df = yf.download(symbol, start=start_date, end=end_date)
        df['OpenInterest'] = 0
        return bt.feeds.PandasData(dataname=df)
    elif data_source == 'csv':
        df = pd.read_csv(symbol, index_col='Date', parse_dates=True)
        df['OpenInterest'] = 0
        return bt.feeds.PandasData(dataname=df)
    else:
        raise ValueError("Unsupported data source")
