#!/usr/bin/env python3
import pickle
import sys

from get_histogram import get_histogram

energies = [0.5, 1, 1.5, 2]
max_energy = max(energies)
bin_size = .05
nbins = int(max_energy / bin_size)
ncase = 1e4

hist_data = [
    get_histogram(int(energy / bin_size), ncase, nbins, max_energy)
    for energy in energies
]

with open(sys.argv[1], "wb") as f:
    pickle.dump({"energies": energies, "hist_data": hist_data}, f)
