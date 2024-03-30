import numpy as np
import pandas as pd
import yfinance as yf
import fin_data_factory as fdf
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq
from scipy.interpolate import griddata
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = 'jupyterlab'

# Main function to fetch data and plot the volatility surface
def plot_vol_surface(chain, fileName):
    chain = chain.dropna()
    r = 0.01  # Assume a constant risk-free rate
    strikes = []
    maturities = []
    vols = []

    for _, row in chain.iterrows():
        K = row['strike']
        T = row['T']
        iv = row['impliedVolatility']
        if np.isnan(iv) or iv == 0:
            continue
        strikes.append(K)
        maturities.append(T)
        vols.append(iv)

    # Convert lists to numpy arrays for griddata function
    strikes = np.array(strikes)
    maturities = np.array(maturities)
    vols = np.array(vols)

    # Create grid
    ti = np.linspace(maturities.min(), maturities.max(), 100)
    xi = np.linspace(strikes.min(), strikes.max(), 100)
    XI, TI = np.meshgrid(xi, ti)

    # Interpolate vols onto grid
    VI = griddata((maturities, strikes), vols, (TI, XI), method='cubic')
    # Create a 3D surface plot
    fig = go.Figure(data=[go.Surface(z=VI, x=XI, y=TI)])
    fig.update_layout(title='Volatility Surface', autosize=True,
                      scene=dict(
                          xaxis_title='Strike Price',
                          yaxis_title='Time to Expiration (Years)',
                          zaxis_title='Implied Volatility'),
                      margin=dict(l=65, r=50, b=65, t=90))
    fig.write_html(f"{fileName}.html")