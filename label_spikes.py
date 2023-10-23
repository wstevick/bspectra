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
print("Enter potential spikes. EOF to exit")
candidates = [source_energy - eval(v.strip()) for v in sys.stdin]

found = []

for idx, candidate in enumerate(candidates):
    closest_ray = np.argmin(np.abs(candidate - ray_energies))

    closest_name = ray_names[closest_ray]
    closest_energy = ray_energies[closest_ray]

    if abs(closest_energy - candidate) > bin_size / 2:
        print(
            f"skipping #{idx} because |{candidate} - {closest_energy}| > {bin_size / 2} for closest X-Ray {closest_name!r}"
        )
    else:
        found.append((closest_name, closest_energy))

pprint(found)
