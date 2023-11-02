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

# because of how fill_between works, we need an extra bin
xs = np.arange(nbins + 1) * bin_size
bin_centers = xs[:-1] + bin_size * 0.5

plt.yscale("log")
plt.xlabel("KeV")

# the hsitogram plot, with errobars
plt.errorbar(bin_centers, heights, errors, 0, fmt="none", color="red")
# because of how fill_between works, the last bin is ignored, so we add a dummy bin at the end
plt.fill_between(xs, np.append(heights, -1), step="post")

# plot visible X-ray spikes
x_rays = []

for name, x_ray in x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name,
        (pos_on_plot, heights[np.argmin(np.abs(bin_centers - pos_on_plot))]),
    )
    plt.axvline(pos_on_plot, color="purple")

plt.show()
