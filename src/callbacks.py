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
    Input(component_id='sbsp-selection', component_property='value'),
    Input(component_id='col-abs-switch', component_property='on'),
    Input(component_id='col-log-switch', component_property='on'),
    Input(component_id='snap-button', component_property='n_clicks'),
    Input(component_id="full-trace", component_property='relayoutData')
]

update_trace_outputs = [
    Output(component_id="full-trace", component_property='figure'),
    Output(component_id='saved-trace', component_property='figure'),
    Output(component_id='var-selection', component_property='options'),
    Output(component_id='col-selection', component_property='options')
]

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
            return {}, {}, {}, {}

        if ((triggered_id == "file-selection") or \
            (triggered_id == "import-selection")
        ):
            data = \
                load_file(file_name) if imprt == 'interpolate' else \
                load_file(
                    file_name,
                    interpolate=False,
                    interpolate_gradient=False,
                    drop_zeros=False
                )
            self.data = data
            self.valid_keys = create_options_from_list(data.keys())

            recommended_sampling = round(data["t"].size/10_000) #BUG: 10 000 elements on screen max

            print(f"Recommended Sampling rate: {recommended_sampling}") #BUG: what the default sampling should be for full view

        # elif any(triggered_id == key for key in \
        #     ['col-selection', 'col-abs-switch', 'col-log-switch']):
        #     pass

        if triggered_id=="snap-button":
            print("snap!")
            self.saved_fig = go.Figure(self.fig)
            return self.fig, self.saved_fig, self.valid_keys, self.valid_keys

        var = "y" if var is None else var
        col = self.data['e'] if color is None else self.data[color]
        col = np.abs(col) if col_abs else col
        if col_log:
            col = np.log2(col, out=np.zeros_like(col), where=(col!=0))

        self.fig = subsampled_plot(
            self.data["t"], self.data[var], c=col,
            subsample=substep, colorbar=dict(title=color)
        )

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
        else:
            self.range = None


        if not self.range is None:
            self.fig.update_layout(
                xaxis_range=self.range[0],
            )
            if not (triggered_id == "var-selection"):
                self.fig.update_layout(
                    yaxis_range=self.range[1]
                )

        return self.fig, self.saved_fig, self.valid_keys, self.valid_keys

# =========================================================================== #