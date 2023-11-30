#!/usr/bin/env python3
from collections import defaultdict
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

if len(sys.argv) < 4 or sys.argv[3] != 'nolog':  # noqa: PLR2004
    plt.yscale("log")
plt.xlabel("KeV")

# the histogram plot, with errorbars
plt.errorbar(bin_centers, heights, errors, 0, fmt="none", color="red")
# because of how fill_between works, the last bin is ignored, so we add a dummy bin at the end
plt.fill_between(xs, np.append(heights, -1), step="post")

# x-rays in visible spikes
visible_x_rays = [
    (r"$L_2M_1 L_\eta$", 4.23e-2, 10.3082),
    (r"$L_1M_1$", 7.05e-6, 10.9287),
    (r"$L_2M_3 L_{\beta 17}$", 1.61e-3, 10.99),
    (r"$L_1M_2 L_{\beta 4}$", 0.373, 11.2048),
    (r"$L_3N_1 L_{\beta 6}$", 1.68e-2, 11.1564),
    (r"$L_2M_4 L_{\beta 1}$", 1.565, 11.442),
    (r"$L_3N_2$", 1.71e-4, 11.2755),
    (r"$L_3N_3$", 1.73e-4, 11.371),
    (r"$L_1M_3 L_{\beta 3}$", 0.43, 11.6105),
    (r"$L_2M_5$", 8.62e-5, 11.5272),
    (r"$L_3N_4 L_{\beta 15}$", 2.515e-2, 11.564),
    (r"$L_3N_5 L_{\beta 2}$", 0.2267, 11.58212),
    (r"$L_3N_{6,7} L_u$", 1.67e-4, 11.8305),
    #(r"L3 edge", 11.92778),
    (r"$L_2N_2$", 7.43e-7, 13.0894),
    (r"$L_2N_3$", 4.35e-4, 13.18489),
    (r"$L_2N_4 L_{\gamma 1}$", 0.309, 13.3779),
    (r"$L_2N_5$", 0, 13.39601),
    (r"$L_1N_1$", 3.09e-6, 13.5908),
    (r"$L_1N_2 L_{\gamma 2}$", 9.43e-2, 13.71),
    (r"$L_2N_6 L_v$", 1.12e-3, 13.6425),
    (r"$L_2N_7$", 0, 13.6462),
    #(r"L2 edge", 13.74167),
    #("K edge", 80.7347),
    (r"$KN_2 K_{\beta_2^{II}}$", 0.6525, 80.0825),
    (r"$KN_3 K_{\beta_2^I}$", 1.2805, 80.1779),
    (r"$KM_5 K_{\beta_5^I}$", 8.29e-2, 78.5203),
    (r"$KM_4 K_{\beta_5^{II}}$", 6.74e-2, 78.4351),
    (r"$KM_3 K_{\beta 1}$", 5.305, 77.983),
    (r"$KM_2 K_{\beta 3}$", 2.7435, 77.5773),
    (r"$KL_3 K_{\alpha 1}$", 24.535, 68.8069),
    (r"$KL_2 K_{\alpha 2}$", 14.42, 66.993),
]

# group x-rays in the same bin together
bins_with_x_rays = defaultdict(list)
for name, intensity, energy in visible_x_rays:
    pos_on_plot = source_energy - energy
    bins_with_x_rays[np.argmin(np.abs(bin_centers - pos_on_plot))].append((name, intensity, pos_on_plot))

for binid, rays in bins_with_x_rays.items():
    max_intensity = max(intensity for _, intensity, _ in rays)

    # plot x-rays whose intensity is more than a tenth the maximum intensity of all x-rays in the bin
    for name, intensity, pos_on_plot in rays:
        if intensity * 10 < max_intensity:
            continue
        plt.annotate(
            f'{name} ({intensity})',
            (pos_on_plot, heights[binid]),
            rotation=90,
        )
        plt.axvline(pos_on_plot, color="purple")

plt.show()
