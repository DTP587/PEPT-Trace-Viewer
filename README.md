# PEPT Trace Viewer

PEPT trace viewer written with dash. Very rough state at the moment.

Expects raw data in CSV or PKL format. Will automatically spit out .pkl file if .csv file is given. Reads from ./assests/ and the cwd.


## Things to add:

- [ ] Recommended subsampling as a default when file is open.
- [ ] Dynamic subsampling (subsampling is adjusted on zoom in, only plot points in view).
- [ ] Generate requirements.txt
- [ ] Reorder the columns on example_data.pkl so that Y and Color are accurate to file output.
- [ ] Fix/remove interpolation option for time series.
