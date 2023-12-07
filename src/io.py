import numpy as np
import pickle
from scipy.interpolate import interp1d

# --------------------------------------------------------------------------- #

def filter_vals(sets, index):
    return [i[index] for i in sets]

def load_file(
    file_name, order="texyz", interpolate=False, interpolate_gradient=False,
    drop_zeros=False
):
    """Imports raw data files in ascii or pickle from raw trace files"""

    print(f"Loading File: {file_name}")

    # Load in file
    if file_name[-4:] == ".csv":
        # Load csv and dump into pickle file
        with open(file_name, newline='\n') as file:
            _     = file.readline()
            line1 = file.readline()
            if ',' in line1:
                delimiter=','
            else:
                delimiter=' '

        raw = np.genfromtxt(
            file_name, skip_header=1, delimiter=delimiter, dtype=np.float64
        )

        # Expect data in: t, e, x, y, z
        print(raw.shape)

        with open(f"{file_name[:-4]}.pkl", "wb") as datafile:
            pickle.dump(raw, datafile)

    elif file_name[-4:] == ".pkl":
        # load pickle file
        with open(f"{file_name}", "rb") as datafile:
            raw = pickle.load(datafile)
    else:
        raise ValueError(f"Unrecognised file type {file_name}")


    # Order contents according to order kwarg
    if ("texyz" == order):
        traw, e, x, y, z = raw.T
    elif ("txyze" == order):
        traw, x, y, z, e = raw.T
    else:
        ValueError(f"order argument: {order} unrecognised")

    points = traw.shape[0]
    ti = np.arange(points)
    t = traw

    ordered = np.argsort(t)
    t = t[ordered]
    e = e[ordered]
    x = x[ordered]
    y = y[ordered]
    z = z[ordered]

    if interpolate:
        unique_t, unique_i = np.unique(traw, return_index=True)
        interp_t = interp1d(
            unique_i, unique_t, kind='cubic', fill_value="extrapolate"
        )
        t = np.round(interp_t(ti))

    t_derivatives = []

    for derivative in [1, 2]:
        array = np.gradient(t, derivative)

        if interpolate_gradient:
            zeros = array == 0
            mask = np.logical_not(array)
            interp_td = interp1d(
                ti[mask], array[mask], kind="linear", fill_value="extrapolate"
            )
            array[zeros] = interp_td(ti[zeros])

        t_derivatives.append(array)

    tdiff, tddif = t_derivatives

    if drop_zeros:
        rows_to_drop = np.logical_or(tdiff > 0, tddif > 0)
        print(
            f"\nDropping {rows_to_drop.shape[0] - np.sum(rows_to_drop)} "
            "rows due to bad gradient. Turn off this option with "
            "`drop_zeros=False`."
        )
        t, tdiff, tddif, e, x, y, z = filter_vals(
            [t, tdiff, tddif, e, x, y, z], rows_to_drop
        )

    # differences
    xdiff = np.gradient(x)
    ydiff = np.gradient(y)
    zdiff = np.gradient(z)
    ediff = np.gradient(e)

    xvel = xdiff/tdiff
    yvel = ydiff/tdiff
    zvel = zdiff/tdiff
    dedt = ediff/tdiff
    vel  = np.sqrt(xvel**2+yvel**2+zvel**2)
    dvdt = np.gradient(vel)/tddif

    return dict(
        ti=ti, tdiff=tdiff, tddif=tddif,
        t=t, x=x, y=y, z=z,
        e=e, xvel=xvel, yvel=yvel, zvel=zvel, vel=vel,
        dedt=dedt, dvdt=dvdt
    )