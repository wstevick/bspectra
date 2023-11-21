#!/usr/bin/env python3
import gzip
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

# read data from the file given by a command line argument
with gzip.open(
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

if len(sys.argv) < 4 or sys.argv[3] != 'nolog':
    plt.yscale("log")
plt.xlabel("KeV")

# the histogram plot, with errorbars
plt.errorbar(bin_centers, heights, errors, 0, fmt="none", color="red")
# because of how fill_between works, the last bin is ignored, so we add a dummy bin at the end
plt.fill_between(xs, np.append(heights, -1), step="post")

# plot visible X-ray spikes
visible_x_rays = [
    (r"$L_2M_1 L_\eta$", 10.3082),
    (r"$L_1M_1$", 10.9287),
    (r"$L_2M_3 L_{\beta 17}$", 10.99),
    (r"$L_1M_2 L_{\beta 4}$", 11.2048),
    (r"$L_3N_1 L_{\beta 6}$", 11.1564),
    (r"$L_2M_4 L_{\beta 1}$", 11.442),
    (r"$L_3N_2$", 11.2755),
    (r"$L_3N_3$", 11.371),
    (r"$L_1M_3 L_{\beta 3}$", 11.6105),
    (r"$L_2M_5$", 11.5272),
    (r"$L_3N_4 L_{\beta 15}$", 11.564),
    (r"$L_3N_5 L_{\beta 2}$", 11.58212),
    (r"$L_3N_6 L_{u (\prime)}$", 11.8287),
    (r"$L_3N_7 L_u$", 11.8323),
    (r"L3 edge", 11.92778),
    (r"$L_2N_2$", 13.0894),
    (r"$L_2N_3$", 13.18489),
    (r"$L_2N_4 L_{\gamma 1}$", 13.3779),
    (r"$L_2N_5$", 13.39601),
    (r"$L_1N_1$", 13.5908),
    (r"$L_1N_2 L_{\gamma 2}$", 13.71),
    (r"$L_2N_6 L_v$", 13.6425),
    (r"$L_2N_7$", 13.6462),
    (r"L2 edge", 13.74167),
    ("K edge", 80.7347),
    (r"$KN_2 K_{\beta_2^{II}}$", 80.0825),
    (r"$KN_3 K_{\beta_2^I}$", 80.1779),
    (r"$KM_5 K_{\beta_5^I}$", 78.5203),
    (r"$KM_4 K_{\beta_5^{II}}$", 78.4351),
    (r"$KM_3 K_{\beta 1}$", 77.983),
    (r"$KM_2 K_{\beta 3}$", 77.5773),
    (r"$KL_3 K_{\alpha 1}$", 68.8069),
    (r"$KL_2 K_{\alpha 2}$", 66.993),
]

for name, x_ray in visible_x_rays:
    # convert energy to KeV, then calculate the position of the spike caused by the X-ray
    pos_on_plot = source_energy - x_ray
    plt.annotate(
        name,
        (pos_on_plot, heights[np.argmin(np.abs(bin_centers - pos_on_plot))]),
        rotation=90,
    )
    plt.axvline(pos_on_plot, color="purple")

plt.show()
