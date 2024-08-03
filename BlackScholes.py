import numpy as np
from scipy.stats import norm


class BlackScholes:
    """
    Black-Scholes model for European Options.
    """

    def __init__(self, S, K, T, r, sigma):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma

    def _d1_d2(self):
        """
        Calculates and returns the d1 and d2 parameters used in Black-Scholes formula.
        """
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        return d1, d2

    def call_option_price(self):
        """
        Calculate and return the Black-Scholes price for a European call option.
        """
        d1, d2 = self._d1_d2()
        return self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)

    def put_option_price(self):
        """
        Calculate and return the Black-Scholes price for a European put option.
        """
        d1, d2 = self._d1_d2()
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)