from dash.dependencies import Input, Output
from dash import ctx

import plotly.graph_objects as go

import numpy as np

from .io import load_file
from .plotting import subsampled_plot
from .utils import create_options_from_list

update_trace_inputs = [
    Input(component_id='import-selection', component_property='value'),
    Input(component_id='file-selection', component_property='value'),
    Input(component_id='var-selection', component_property='value'),
    Input(component_id='col-selection', component_property='value'),
    Input(component_id='sbsp-input', component_property='value'),
    Input(component_id='col-abs-switch', component_property='on'),
    Input(component_id='col-log-switch', component_property='on'),
    Input(component_id='snap-button', component_property='n_clicks'),
    Input(component_id='full-trace', component_property='relayoutData')
]

update_trace_outputs = [
    Output(component_id='full-trace', component_property='figure'),
    Output(component_id='saved-trace', component_property='figure'),
    Output(component_id='sbsp-input', component_property='value'),
    Output(component_id='var-selection', component_property='options'),
    Output(component_id='col-selection', component_property='options')
]

def update_trace_returns(self, **kwargs):
    for key, value in kwargs.items():
        if (("clear" == key) and value):
            return {}, {}, None, {}, {}
        elif ("fig" == key):
            self.fig = value
        elif ("saved_fig" == key):
            self.saved_fig = value
        elif ("subsampling" == key):
            self.subsampling = value
        elif ("valid_keys" == key):
            self.valid_keys = value

    return self.fig, self.saved_fig, self.subsampling, self.valid_keys, self.valid_keys

# =========================================================================== #

def get_callbacks(self, app):

    @app.callback(
        update_trace_outputs,
        update_trace_inputs
    )
    def update_trace_callback(
        imprt, file_name, var, color, substep, col_abs, col_log, n_snap,
        relayoutData
    ):

        triggered_id = ctx.triggered_id

        if file_name is None:
            return update_trace_returns(self, clear=True)

        if (
            (triggered_id == "file-selection") or \
            (triggered_id == "import-selection")
        ):
            data = load_file(file_name, order=imprt)

            self.data = data
            self.valid_keys = create_options_from_list(data.keys())

            # recommended sampling rate, avoid > 12_000 elements on screen
            self.subsampling = np.ceil(data["t"].size/12_000)

        if triggered_id == "snap-button":
            print("snap!")
            self.saved_fig = go.Figure(self.fig)
            return update_trace_returns(self)

        var = "y" if var is None else var
        col = self.data['e'] if color is None else self.data[color]
        col = np.abs(col) if col_abs else col
        if col_log:
            col = np.log2(col, out=np.zeros_like(col), where=(col!=0))

        plot_x = self.data["t"]
        plot_y = self.data[var]
        plot_c = col

        relayout_args = list(relayoutData.keys())

        if all(
            item in relayout_args \
            for item in ["xaxis.range[0]", "yaxis.range[0]"] \
        ):
            self.range = [
                (
                    relayoutData["xaxis.range[0]"],
                    relayoutData["xaxis.range[1]"]
                ),
                (
                    relayoutData["yaxis.range[0]"],
                    relayoutData["yaxis.range[1]"]
                )
            ]
            idx = (plot_x > self.range[0][0]) & (plot_x < self.range[0][1])
            plot_x = plot_x[idx]
            plot_y = plot_y[idx]
            plot_c = plot_c[idx]
        else:
            self.range = None

        if triggered_id == "sbsp-input":
            self.subsampling = substep
        else:
            # recommended sampling rate, avoid > 12_000 elements on screen
            self.subsampling = np.ceil(plot_x.size/12_000)

        self.fig = subsampled_plot(
            plot_x, plot_y, c=plot_c,
            subsample=self.subsampling, colorbar=dict(title=color)
        )

        if not self.range is None:
            self.fig.update_layout(
                xaxis_range=self.range[0],
            )
            if not (triggered_id == "var-selection"):
                self.fig.update_layout(
                    yaxis_range=self.range[1]
                )

        return update_trace_returns(self)