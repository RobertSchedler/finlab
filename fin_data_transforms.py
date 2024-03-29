import numpy as np
import pandas as pd
import yfinance as yf
import fin_data_factory as fdf
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq


# Function to calculate implied volatility
def implied_volatility(option_price, S, K, T, r, option_type='call'):
    def bs_price(sigma):
        d1 = (np.log(S / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return price - option_price

    try:
        implied_vol = brentq(bs_price, 1e-6, 1)
    except ValueError:
        implied_vol = np.nan
    return implied_vol

# Main function to fetch data and plot the volatility surface
def plot_vol_surface(ticker_symbol):
    calls = fdf.get_options_chain(ticker_symbol)
    S = yf.Ticker(ticker_symbol).history(period="1d")['Close'][-1]  # Current stock price
    r = 0.01  # Assume a constant risk-free rate

    strikes = []
    maturities = []
    vols = []

    for _, row in calls.iterrows():
        K = row['strike']
        T = (pd.to_datetime(row['ExpirationDate']) - pd.Timestamp.now()).days / 365
        price = row['lastPrice']

        iv = implied_volatility(price, S, K, T, r)
        if np.isnan(iv) or iv == 0:
            continue

        strikes.append(K)
        maturities.append(T)
        vols.append(iv)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(maturities, strikes, vols, zdir='z', s=20, c='b', depthshade=True)
    ax.set_xlabel('Time to Expiration (Years)')
    ax.set_ylabel('Strike Price')
    ax.set_zlabel('Implied Volatility')
    ax.set_title('Volatility Surface for ' + ticker_symbol)

    plt.show()