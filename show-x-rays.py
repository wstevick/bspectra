#!/usr/bin/env python3
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np

# read data from the file given by a command line argument
with open(sys.argv[1], "rb") as f:
    data = pickle.load(f)
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

xs = (np.arange(nbins) + 1 / 2) * bin_size

plt.yscale("log")
plt.xlabel("KeV")

# the actual hsitogram plot, with errobars
plt.errorbar(xs, heights, errors, 0, fmt="none", color="red")
plt.bar(xs, heights, width=bin_size)

# plot visible X-ray spikes
x_rays = [
    ("L1M3", 11.6105),
    ("L3N3", 11.371),
    ("L3N1", 11.1564),
    ("L2N4", 13.3779),
    ("L3N7", 11.8323),
    ("L2N6", 13.6425),
    ("KL2", 66.993),
    ("KL3", 68.8069),
    ("KM3", 77.983),
    ("KM2", 77.5773),
    ("KN2", 80.0825),
    ("K edge", 80.7347),
    ("KM4", 78.4351),
    ("KM5", 78.5203),
    ("KN4", 80.371),
    ("L2M1", 10.3082),
]

for name, x_ray in x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name, (pos_on_plot, heights[np.argmin(np.abs(xs - pos_on_plot))])
    )

plt.show()
