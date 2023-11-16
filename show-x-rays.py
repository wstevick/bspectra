#!/usr/bin/env python3
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

# read data from the file given by a command line argument
with open(
    sys.stdin.fileno() if sys.argv[1] == "-" else sys.argv[1], "rb"
) as f:
    data = pickle.load(f)
energies = data["energies"]
hist_data = data["hist_data"]

# the file has multiple plots stored in it
# the next command line argument says which to use
plotnum = int(sys.argv[2])
heights = unp.nominal_values(hist_data[plotnum])
errors = unp.std_devs(hist_data[plotnum])
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
    (r"$L_2M_1$", 10.3082),
    (r"$L_1M_1$", 10.9287),
    (r"$L_2M_3$", 10.99),
    (r"$L_1M_2$", 11.2048),
    (r"$L_3N_1$", 11.1564),
    (r"$L_2M_4$", 11.442),
    (r"$L_3N_2$", 11.2755),
    (r"$L_3N_3$", 11.371),
    (r"$L_1M_3$", 11.6105),
    (r"$L_2M_5$", 11.5272),
    (r"$L_3N_4$", 11.564),
    (r"$L_3N_5$", 11.58212),
    (r"$L_3N_6$", 11.8287),
    (r"$L_3N_7$", 11.8323),
    # (r"L3 edge", 11.92778),
    (r"$L_2N_2$", 13.0894),
    (r"$L_2N_3$", 13.18489),
    (r"$L_2N_4$", 13.3779),
    (r"$L_2N_5$", 13.39601),
    (r"$L_1N_1$", 13.5908),
    (r"$L_1N_2$", 13.71),
    (r"$L_2N_6$", 13.6425),
    (r"$L_2N_7$", 13.6462),
    # (r"L2 edge", 13.74167),
]

for name, x_ray in visible_x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name,
        (pos_on_plot, heights[np.argmin(np.abs(bin_centers - pos_on_plot))]),
    )
    plt.axvline(pos_on_plot, color="purple")

plt.show()
