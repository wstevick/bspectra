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
    ("L1M3 L beta 3", 11.6105),
    ("L3N3 L beta 6", 11.371),
    ("L3N1 L beta 6", 11.1564),
    ("L2N4 L gamma 1", 13.3779),
    ("L3N7 L u (mu?)", 11.8323),
    ("L2N6 L v (nu?)", 13.6425),
    ("KL2 K alpha 2", 66.993),
    ("KL3 K alpha 1", 68.8069),
    ("KM3 K beta 1", 77.983),
    ("KM2 K beta 3", 77.5773),
    ("KN2 K beta^II_2", 80.0825),
    ("K edge ?", 80.7347),
    ("KM4 K beta^II_5", 78.4351),
    ("KM5 K beta^I_5", 78.5203),
    ("KN4 K beta^II_4/K beta 4", 80.371),
    ("L2M1 L eta", 10.3082),
]

for name, x_ray in x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name, (pos_on_plot, heights[np.argmin(np.abs(xs - pos_on_plot))])
    )

plt.show()
