import numpy as np
from scipy.stats import norm


def black_scholes_call(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price of a European call option.

    Parameters:
    - S: Current stock price
    - K: Strike price of the option
    - T: Time to expiration in years
    - r: Risk-free interest rate (annual)
    - sigma: Volatility of the stock's returns (annual)

    Returns:
    - Call option price
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the call option price
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

    return call_price

def black_scholes_put(S, K, T, r, sigma):
    """
    Calculate the Black-Scholes price of a European put option.

    Parameters:
    - S: Current stock price
    - K: Strike price of the option
    - T: Time to expiration in years
    - r: Risk-free interest rate (annual)
    - sigma: Volatility of the stock's returns (annual)

    Returns:
    - Put option price
    """
    # Calculate d1 and d2
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    # Calculate the put option price
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return put_price