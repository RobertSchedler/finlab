import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata


class VolatilitySurface:

    def __init__(self, option_chain):
        self.chain = option_chain

    def plot_surface(self, file_name, plot_points=True):
        T = self.chain['T']
        K = self.chain['K']
        Vol = self.chain['impliedVolatility']

        if plot_points:
         # Create the 3D scatter plot
            plot = go.Scatter3d(x=T, y=K, z=Vol, mode='markers')
        else:
         # Create a 3D surface plot
            z_grid = self.interpolate_values(T, K, Vol)
            plot = go.Surface(x=T, y=K, z=z_grid)

        fig = go.Figure(data=[plot])

        fig.update_layout(
            title='Volatility Surface',
            scene=dict(
                xaxis_title='Time to Maturity (T)',
                yaxis_title='Strike Price (K)',
                zaxis_title='Implied Volatility'),
            autosize=True
        )

        # Save the plot as an HTML file
        fig.write_html(f"{file_name}.html")
        print(f"Plot saved as {file_name}.html")


    def interpolate_values(self, T, K, Vol):
        # Create a grid and interpolate data
        x = np.linspace(T.min(), T.max(), num=500)
        y = np.linspace(K.min(), K.max(), num=500)
        x_grid, y_grid = np.meshgrid(x, y)
        z_grid = griddata((T, K), Vol, (x_grid, y_grid), method='cubic')
        return z_grid