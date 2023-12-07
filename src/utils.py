"""
utils.py

Just a list of some functions which help viewing or redistributing arrays.
"""
import numpy as np
from scipy.ndimage import distance_transform_edt

def create_options_from_list(items):
    if all(isinstance(item, tuple) for item in items):
        return [ {'label': item[0], 'value': item[1]} for item in items]
    elif all(isinstance(item, str) for item in items):
        return [ {'label': item, 'value': item} for item in items]

def nearest_neighbour_spacing(arr, spacing):
    """Finds nearest neighbours of a certain linear spacing, and returns them
    as a numpy array of indexes."""
    nmin = int(arr[0]//spacing) + 1
    nmax = int(arr[-1]//spacing) + 1
    idx = np.zeros(nmax - nmin + 1, dtype=int)
    n = nmin
    dprev = spacing
    xprev = -nmin*spacing
    for i, x in enumerate(arr):
        d = abs(n*spacing - x)
        if d > dprev:
            idx[n-nmin] = i-1
            if n < len(arr):
                n += 1
                d = abs(n*spacing - x)
                dprev += abs(n*spacing - xprev)
        else:
            dprev = d
        xprev = x
    idx[-1] = len(arr)-1
    return idx

def create_grid(spacing, x_data, y_data):
    """Creates a grid from x and y data, with specified spacing."""
    x_max = spacing*np.ceil(x_data.max()/spacing + 1)
    y_max = spacing*np.ceil(y_data.max()/spacing + 1)

    
    x_min = spacing*np.floor(x_data.min()/spacing - 1) \
        if x_data.min() < 0 else 0
    y_min = spacing*np.floor(y_data.min()/spacing - 1) \
        if y_data.min() < 0 else 0

    xs = np.arange(x_min, x_max, spacing)
    ys = np.arange(y_min, y_max, spacing)

    return xs, ys


def bin_hits(val, rc, yc, spacing, minh=None, fill=None):

    r_steps, y_steps = create_grid(spacing, rc, yc)

    hits, r_bins, y_bins = \
        np.histogram2d(rc, yc, bins = [r_steps, y_steps])

    if minh is not None:
        hits[hits<minh] = fill

    weighted_hits, _, _ = \
        np.histogram2d(rc, yc, bins = [r_steps, y_steps], weights=val)

    # Compute sum
    av_hits = np.zeros_like(hits)
    av_hits[hits!=0] = weighted_hits[hits!=0]/hits[hits!=0]
    return [av_hits, hits], [r_steps, y_steps]


def fill_invalid(data, invalid=None):
    """
    Replace the value of invalid 'data' cells (indicated by 'invalid') 
    by the value of the nearest valid data cell

    Input:
        data:    numpy array of any dimension
        invalid: a binary array of same shape as 'data'. True cells set where data
                 value should be replaced.
                 If None (default), use: invalid  = np.isnan(data)

    Output: 
        Return a filled array. 
    """
    if invalid is None: invalid = np.isnan(data)

    ind = distance_transform_edt(invalid, return_distances=False, return_indices=True)
    return data[tuple(ind)]