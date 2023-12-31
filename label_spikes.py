#!/usr/bin/env python3
import csv
import pprint
import sys

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

found = []

for spike in visible_spikes:
    # iterate over every pair of spikes, counting
    for idx1, energy1 in enumerate(ray_energies):
        for idx2, energy2 in enumerate(ray_energies[idx1:]):
            # determine if it's a commpound spike
            if abs(energy1 + energy2 - spike) <= bin_size / 2:
                # if so add the two spikes that were added to make it to the list
                found.append(
                    [
                        (ray_names[idx], round(energy, 10))
                        for (idx, energy) in [(idx1, energy1), (idx2, energy2)]
                    ]
                )

    # how far is the spike from each x-ray
    distance_to_x_rays = np.abs(ray_energies - spike)
    # which x-rays are close enough to be within the spike's bin
    rays_in_bin = distance_to_x_rays <= bin_size / 2
    # if none of the x-rays are in the spike's bin, print the spike and say which was closest
    if not np.any(rays_in_bin):
        print(
            f"{spike} skipped because {ray_names[np.argmin(distance_to_x_rays)]!r} is more than {bin_size / 2} KeV away"
        )
        continue
    # add all of the x-rays in the spike's bin to found
    found.extend(
        (name, round(energy, 10))
        for name, energy, in_bin in zip(ray_names, ray_energies, rays_in_bin)
        if in_bin
    )

pprint.pprint(found)
