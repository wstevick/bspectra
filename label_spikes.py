#!/usr/bin/env python3
import csv
import sys
from pprint import pprint

import numpy as np

with open("gold.tsv", newline="") as f:
    f.readline()
    data = list(csv.reader(f, delimiter="\t"))

ray_names = [ray[2] for ray in data]
ray_energies = np.array([float(ray[3]) for ray in (data)]) * 1e-3

source_energy = float(input("Source energy of the simulation (KeV): "))
bin_size = float(input("Bin size of the simulation (KeV): "))
print("Enter visible spikes. EOF to exit")
visible_spikes = [source_energy - eval(v.strip()) for v in sys.stdin]

pprint(
    [
        (name, energy)
        for spike in visible_spikes
        for name, energy, in_bin in zip(
            ray_names,
            ray_energies,
            np.abs(ray_energies - spike) <= bin_size / 2,
        )
        if in_bin
    ]
)
