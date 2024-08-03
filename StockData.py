import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq


class StockData:
    """
    Fetches and holds stock data along with options chain using Yahoo Finance.
    """

    def __init__(self, ticker_symbol):
        self.ticker = yf.Ticker(ticker_symbol)
        self.stock_data = None
        self.options_chain = None

    def fetch_stock_data(self, start_date, end_date):
        """
        Fetches historical stock data.

        Parameters:
        - start_date : The start date for the data in 'YYYY-MM-DD' format
        - end_date : The end date for the data in 'YYYY-MM-DD' format

        Stores the stock data in self.stock_data
        """
        self.stock_data = yf.download(self.ticker.info["symbol"], start=start_date, end=end_date)

    def fetch_option_chain(self):
        """
        Fetches option chains

        Stores the fetched option chains in self.option_chain
        """
        current_price = self.ticker.history(period='1d')['Close'][-1]
        option_dates = self.ticker.options

        calls, puts = pd.DataFrame(), pd.DataFrame()

        for date in option_dates:
            option_chain = self.ticker.option_chain(date)
            option_chain.calls['expirationDate'] = date
            option_chain.puts['expirationDate'] = date
            calls = pd.concat([calls, option_chain.calls])
            puts = pd.concat([puts, option_chain.puts])

        calls['optionType'] = 'Call'
        puts['optionType'] = 'Put'

        self.options_chain = pd.concat([calls, puts]).reset_index(drop=True)
        self.options_chain['P'] = (self.options_chain['bid'] + self.options_chain['ask']) / 2.0
        self.options_chain['S'] = current_price
        self.options_chain['K'] = self.options_chain['strike']
        self.options_chain['T'] = ((pd.to_datetime(self.options_chain['expirationDate'], utc=True)
                                    - pd.Timestamp.now(tz='UTC')).dt.days / 365).dropna()
        self.options_chain['R'] = 0.04
        self.options_chain['impliedVolatility'] = self.options_chain.apply(self.implied_volatility, axis=1)
        self.options_chain = self.options_chain[self.options_chain['volume'] > 1].dropna()

    def implied_volatility(self, row):
        """
        Calculates and returns implied volatility

        Returns: Implied Volatility
        """

        def price_diff(volatility):
            d1 = (np.log(row['S'] / row['K']) +
                  (row['R'] + 0.5 * volatility ** 2) * row['T']) / (volatility * np.sqrt(row['T']))
            d2 = d1 - volatility * np.sqrt(row['T'])

            if row['optionType'] == 'Call':
                price = row['S'] * norm.cdf(d1) - row['K'] * np.exp(-row['R'] * row['T']) * norm.cdf(d2)
            else:
                price = row['K'] * np.exp(-row['R'] * row['T']) * norm.cdf(-d2) - row['S'] * norm.cdf(-d1)
            return price - row['P']

        try:
            return brentq(price_diff, 1e-6, 100)
        except ValueError:
            return np.nan