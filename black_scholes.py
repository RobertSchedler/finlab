import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq

def black_scholes_call(S, K, T, r, sigma):

    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the call option price
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return call_price

def black_scholes_put(S, K, T, r, sigma):

    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the put option price
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return put_price

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
        implied_vol = brentq(bs_price, 1e-6, 10)
    except ValueError:
        implied_vol = np.nan
    return implied_vol