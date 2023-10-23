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
    (11.371, "L3N3"),
    (11.6105, "L1M3"),
    (66.993, "KL2"),
    (68.8069, "KL3"),
    (77.57730000000001, "KM2"),
    (77.983, "KM3"),
    (80.0825, "KN2"),
    (80.7347, "K edge"),
]

for x_ray, name in x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name, (pos_on_plot, heights[np.argmin(np.abs(xs - pos_on_plot))])
    )

plt.show()
