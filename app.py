import os
import json

from src.utils import create_options_from_list

from dash import Dash
import plotly.graph_objects as go

# --------------------------------------------------------------------------- #

# add any searchable dirs in here
SEARCH_DIRS = [
    os.getcwd(),
    os.path.dirname(__file__) + os.sep + "assets"
]

SEARCH_FILES = []
for directory in SEARCH_DIRS:
    for file in os.listdir(directory):
        SEARCH_FILES.append(directory + os.sep + file)

EXTERNAL_STYLESHEETS = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
]

DOWNSAMPLING_OPTIONS = create_options_from_list([
    "1", "2", "5", "10", "20", "50", "100", "200", "500", "1000", "2000"
])

IMPORT_TYPE_OPTIONS = create_options_from_list([
    'raw', 'interpolate'
])

FILE_OPTIONS = create_options_from_list([
    (os.path.basename(file), file) for file in SEARCH_FILES \
    if any([".csv" in file, ".pkl" in file])
])

# --------------------------------------------------------------------------- #

class PEPT_dash:
    def __init__(self):
        self.data = None
        self.fig = {}
        self.saved_fig = {}
        self.xrange = None
        self.valid_keys = None

        self.options = {
            "file-selection": FILE_OPTIONS,
            "sbsp-selection": DOWNSAMPLING_OPTIONS,
            "import-selection": IMPORT_TYPE_OPTIONS
        }

    def create_layout(self, app):
        from src.layout import layout_from_options
        app.layout = layout_from_options(**self.options)

    from src.callbacks import get_callbacks

# --------------------------------------------------------------------------- #

plotter = PEPT_dash()

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

plotter.create_layout(app)
plotter.get_callbacks(app)

if __name__ == '__main__':
    app.run(
        debug=True
    )