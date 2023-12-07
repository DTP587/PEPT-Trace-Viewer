# PEPT Trace Viewer

PEPT trace viewer written with dash. Very rough state at the moment.

Expects raw data in CSV or PKL format. Will automatically spit out .pkl file if .csv file is given. Reads from ./assests/ and the cwd.


## Things to add:

-[x] Recommended subsampling as a default when file is open.
-[x] Dynamic subsampling (subsampling is adjusted on zoom in, only plot points in view).
-[x] Generate requirements.txt
	- Make it into an actual package
-[x] Reorder the columns on example_data.pkl so that Y and Color are accurate to file output.
-[x] Fix/remove interpolation option for time series.
	- Changed interpolation to user-defined order of rows.