"""
plotting.py

Plotting functions for matplotlib and plotly.
"""
import numpy as np
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from dash import Dash, html, dcc, ctx
from dash.dependencies import Input, Output 
import dash_bootstrap_components as dbc
import dash_daq as daq

DEFAULT_COLOR = "blue"

# --------------------------------------------------------------------------- #

def plot_grid(xx, yy, z, label=None, **options):
    fig = plt.figure(figsize=[6, 6.5])
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    mesh = ax.pcolormesh(xx, yy, z, rasterized=True, **options)
    ax.autoscale_view(True)
    ax.grid(False)
    plt.colorbar(mesh, label=label)
    return fig, ax

# --------------------------------------------------------------------------- #

def return_plot(fig, show=True, return_fig=False, save_path=None):
    if return_fig:
        return fig

    if save_path:
        fig.write_html(save_path)
        return None

    if show:
        fig.show()
        return None

def simple_plot(
    x, y, c=DEFAULT_COLOR, colorbar=None,
    show=True, return_fig=False, save_path=None
):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            name="y",
            mode="markers",
            marker=dict(
                color=c if isinstance(c, np.ndarray) else c,
                colorbar=colorbar
            ),
        )
    )

    return return_plot(
        fig, show=show, return_fig=return_fig, save_path=save_path
    )

def subsampled_plot(
     x, y, c=DEFAULT_COLOR, subsample=None, colorbar=None
):
    default_subs = round(x.size/10_000)

    subs = int(default_subs if subsample is None else subsample)

    return go.FigureWidget(simple_plot(
        x[::subs], y[::subs], c=c[::subs], return_fig=True, colorbar=colorbar
    ))

# --------------------------------------------------------------------------- #