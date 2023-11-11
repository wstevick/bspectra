#!/usr/bin/env python3
import json
import sys

import matplotlib.pyplot as plt
import numpy as np

from x_rays import Decay

# read data from the file given by a command line argument
with open(sys.argv[1]) as f:
    data = json.load(f)
energies = data["energies"]
hist_data = data["hist_data"]

# the file has multiple plots stored in it
# the next command line argument says which to use
plotnum = int(sys.argv[2])
heights, errors = hist_data[plotnum]
source_energy = energies[plotnum] * 1e3

# work out the simulation paramaters (in KeV)
max_energy = max(energies) * 1e3
(nbins,) = heights.shape
bin_size = max_energy / nbins

# because of how fill_between works, we need an extra bin
xs = np.arange(nbins + 1) * bin_size
bin_centers = xs[:-1] + bin_size * 0.5

plt.yscale("log")
plt.xlabel("KeV")

# the histogram plot, with errorbars
plt.errorbar(bin_centers, heights, errors, 0, fmt="none", color="red")
# because of how fill_between works, the last bin is ignored, so we add a dummy bin at the end
plt.fill_between(xs, np.append(heights, -1), step="post")

# plot visible X-ray spikes
visible_x_rays = [
    ("L2M1", 10.3082),
    ("L1M1", 10.9287),
    ("L2M3", 10.99),
    ("L1M2", 11.2048),
    ("L3N1", 11.1564),
    ("L2M4", 11.442),
    ("L3N2", 11.2755),
    ("L3N3", 11.371),
    ("L1M3", 11.6105),
    ("L2M5", 11.5272),
    ("L3N4", 11.564),
    ("L3N5", 11.58212),
    ("L3N6", 11.8287),
    ("L3N7", 11.8323),
    # ("L3 edge", 11.92778),
    ("L2N2", 13.0894),
    ("L2N3", 13.18489),
    ("L2N4", 13.3779),
    ("L2N5", 13.39601),
    ("L1N1", 13.5908),
    ("L1N2", 13.71),
    ("L2N6", 13.6425),
    ("L2N7", 13.6462),
    # ("L2 edge", 13.74167),
]

for name, x_ray in visible_x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        f"${Decay.latex_format_iupac(name)}$",
        (pos_on_plot, heights[np.argmin(np.abs(bin_centers - pos_on_plot))]),
    )
    plt.axvline(pos_on_plot, color="purple")

plt.show()
