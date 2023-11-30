#!/usr/bin/env python3
import gzip
import pickle
import sys

from get_histogram import get_histogram

# main program variables
# these are what you tweak to alter the simulation
energies = [0.5, 1, 1.5, 2]
nbins = 200
bin_size = max_energy / nbins
ncase = 1e5

max_energy = max(energies)

hist_data = [
    get_histogram(int(energy / bin_size), ncase, nbins, max_energy)
    for energy in energies
]

with gzip.open(
    sys.stdout.fileno() if sys.argv[1] == "-" else sys.argv[1], "wb"
) as f:
    pickle.dump({"energies": energies, "hist_data": hist_data}, f)
