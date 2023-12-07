# PEPT Trace Viewer

PEPT trace viewer written with dash. Very rough state at the moment.

Expects raw data in CSV or PKL format. Will automatically spit out .pkl file if .csv file is given. Reads from ./assests/ and the cwd.

## Usage

1. Install dependencies
2. Run app.py with python from a directory or add trace files to assets. You should get the following output:
```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "dash_app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```
4. Navigate to the host page using a browser (normally `http://127.0.0.1:8050/`).
5. Select file & go

## Things to add:

<<<<<<< HEAD
-[x] Recommended subsampling as a default when file is open.
-[x] Dynamic subsampling (subsampling is adjusted on zoom in, only plot points in view).
-[x] Generate requirements.txt
	- Make it into an actual package
-[x] Reorder the columns on example_data.pkl so that Y and Color are accurate to file output.
-[x] Fix/remove interpolation option for time series.
	- Changed interpolation to user-defined order of rows.
