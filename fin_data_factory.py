import yfinance as yf
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
def get_stock_data(ticker_symbol, start_date, end_date):
    """
    Fetches historical stock data for a given ticker symbol from Yahoo Finance.

    Parameters:
    - ticker_symbol: The ticker symbol of the stock (e.g., 'AAPL' for Apple Inc.).
    - start_date: The start date for the data in 'YYYY-MM-DD' format.
    - end_date: The end date for the data in 'YYYY-MM-DD' format.

    Returns:
    - A pandas DataFrame containing the historical stock data.
    """
    # Fetch the data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    return stock_data


def get_options_chain(ticker_symbol):
    """
    Fetches the options chain for a given ticker symbol from Yahoo Finance.

    Parameters:
    - ticker_symbol: The ticker symbol of the stock (e.g., 'AAPL' for Apple Inc.).
    - expiration_date: The expiration date for the options in 'YYYY-MM-DD' format.
                      If None, fetches available expiration dates.

    Returns:
    - A tuple containing two pandas DataFrames: (calls, puts) for the specified expiration date.
      If expiration_date is None, returns the list of available expiration dates.
    """
    ticker = yf.Ticker(ticker_symbol)

    def get_current_price(ticker_symbol):
        ticker = yf.Ticker(ticker_symbol)
        # Fetch the current price
        current_price = ticker.history(period='1d')['Close'][-1]
        return current_price

    S = get_current_price(ticker_symbol)
    # Get all available expiration dates
    exp_dates = ticker.options

    # Initialize empty DataFrames for calls and puts
    all_calls = pd.DataFrame()
    all_puts = pd.DataFrame()
    # Iterate through all available expiration dates
    for exp_date in exp_dates:
        # Fetch the options chain for the current expiration date
        options_chain = ticker.option_chain(exp_date)

        # Extract calls and puts
        calls = options_chain.calls
        puts = options_chain.puts

        # Add an expiration date column to calls and puts
        calls['expirationDate'] = exp_date
        puts['expirationDate'] = exp_date

        # Append the current calls and puts to the all_calls and all_puts DataFrames
        all_calls = pd.concat([all_calls, calls], ignore_index=True)
        all_puts = pd.concat([all_puts, puts], ignore_index=True)

    # Now, all_calls and all_puts DataFrames contain the options data for all expiration dates

    # If you want to combine calls and puts into a single DataFrame with a type indicator:
    all_calls['optionType'] = 'Call'
    all_puts['optionType'] = 'Put'
    all_options = pd.concat([all_calls, all_puts], ignore_index=True).reset_index(drop=False).dropna()
    all_options['P'] = (all_options['bid']+all_options['ask'])/2.0
    all_options['S'] = S
    all_options['K'] = all_options['strike']
    all_options['T'] = ((pd.to_datetime(all_options['expirationDate'], utc=True) - pd.Timestamp.now(tz='UTC')).dt.days / 365).dropna()
    all_options['R'] = 0.04
    all_options['OT'] = all_options['optionType']
    all_options['impliedVolatility'] = all_options.apply(implied_volatility, axis=1)



    return all_options.where(all_options['volume'] > 1000).dropna()

def implied_volatility(row):
    P = row['P']
    S = row['S']
    K = row['K']
    T = row['T']
    R = row['R']
    OT = row['OT']
    def bs_price(sigma):
        d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)

        if OT == 'Call':
            price = S * norm.cdf(d1) - K * np.exp(-R * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-R * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

        return price - P

    try:
        implied_vol = brentq(bs_price, 1e-6, 100)
    except ValueError:
        implied_vol = np.nan
    return implied_vol