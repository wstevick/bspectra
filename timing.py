#!/usr/bin/env python3
from time import time

from get_histogram import get_histogram

# main program variables
# these are what you tweak to alter the simulation
energies = [0.5, 1, 1.5, 2]
nbins = 200
ncase = 1e5

max_energy = max(energies)
bin_size = max_energy / nbins


for energy in energies:
    print(energy, end=" ")
    start_t = time()
    get_histogram(int(energy / bin_size), ncase, nbins, max_energy)
    print(time() - start_t)
