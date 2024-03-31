import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata

# Main function to fetch data and plot the volatility surface
def plot_vol_surface(chain, fileName, hull = 5):

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(x=chain['T'], y=chain['K'], z=chain['impliedVolatility'],
                               mode='markers',
                               marker=dict(size=4)))

    fig.update_layout(title='Volatility Surface',
                      scene=dict(
                          xaxis_title='Time to Maturity (T)',
                          yaxis_title='Strike Price (K)',
                          zaxis_title='Implied Volatility'),
                      autosize=True)

    # Save the plot as an HTML file
    fig.write_html(f"{fileName}.html")
    print(f"Plot saved as {fileName}.html")