import os
import json

from src.utils import create_options_from_list

from dash import Dash
import dash_bootstrap_components as dbc

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
    dbc.themes.COSMO
]

IMPORT_TYPE_OPTIONS = create_options_from_list([
    'txyze', 'texyz'
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
        self.subsampling = None

        self.options = {
            "file-selection": FILE_OPTIONS,
            "import-selection": IMPORT_TYPE_OPTIONS
        }

    def create_layout(self, app):
        from src.layout import layout_from_options
        app.layout = layout_from_options(**self.options)

    from src.callbacks import get_callbacks

# --------------------------------------------------------------------------- #

plotter = PEPT_dash()

app = Dash(__name__)

plotter.create_layout(app)
plotter.get_callbacks(app)

app.config.external_stylesheets = EXTERNAL_STYLESHEETS

if __name__ == '__main__':
    app.run(
        debug=True
    )