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
source_energy = hist_data[plotnum]

# work out the simulation paramaters
max_energy = max(energies)
(nbins,) = heights.shape
bin_size = nbins / max_energy
print(max_energy, nbins, bin_size)

# the centers of each histogram bin, in KeV
xs = (np.arange(nbins) + 1 / 2) * bin_size * 1e3

plt.yscale("log")

plt.xlabel('KeV')

# the actual hsitogram plot, with errobars
plt.errorbar(xs, heights, errors, 0, fmt='none')
plt.fill_between(xs, heights, step="mid")

plt.show()
