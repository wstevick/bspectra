#!/usr/bin/env python3
import gzip
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

colors = ["blue", "green", "purple"]
xs = (np.arange(100) + 0.5) * 0.70953 / 100

for color, file in zip(colors, sys.argv[1:]):
    with gzip.open(file, "rb") as f:
        data = pickle.load(f)
        plt.plot(xs, unp.nominal_values(data), color=color)

plt.show()
