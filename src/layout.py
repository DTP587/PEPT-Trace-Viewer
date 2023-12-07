from dash import html, dcc
import dash_daq as daq
import dash_bootstrap_components as dbc

TITLE = "Positron Emission Particle Tracking Monitor"

def layout_from_options(**options):
    return html.Div(
        [
            html.H3(TITLE),
            html.Hr(),
            dbc.Row([
                dbc.Col([
                    html.P('Import Type'),
                    dcc.Dropdown(
                        id="import-selection",
                        value="txyze",
                        options=options["import-selection"]
                    )
                ], width=1),
                dbc.Col([
                    html.P('File'),
                    dcc.Dropdown(
                        id="file-selection",
                        options=options["file-selection"]
                    )
                ], width=3),
                dbc.Col([
                    html.P('Y'),
                    dcc.Dropdown(
                        id="var-selection",
                        value='y',
                        clearable=False
                    )
                ], width=1),
                dbc.Col([
                    html.P('Subsample'),
                    dcc.Input(
                        id="sbsp-input",
                        type="number",
                        value=None,
                        min=1,
                        max=5000,
                        step=1,
                        debounce=True
                    )
                ], width=1),
                dbc.Col([
                    html.P('Color'),
                    dcc.Dropdown(
                        id="col-selection",
                        value='e',
                        clearable=False
                    )
                ], width=1),
                dbc.Col([
                    html.P('Color - abs'),
                    daq.BooleanSwitch(
                        id='col-abs-switch',
                        on=False
                    )
                ], width=1),
                dbc.Col([
                    html.P('Color - log'),
                    daq.BooleanSwitch(
                        id='col-log-switch',
                        on=False
                    )
                ], width=1)
            ]),
            dcc.Graph(
                id = "full-trace",
                figure = {}
            ),
            html.Div([ 
                html.Button(
                    'snap',
                    id='snap-button',
                    n_clicks=0
                )
            ]),
            dcc.Graph(
                id = 'saved-trace',
                figure = {}
            ),
            # html.Br(),
        ],
        style={"margin": "20px 0px 0px 20px"} #{"padding": 30}
    )