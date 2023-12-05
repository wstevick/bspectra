#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

colors = ["blue", "green", "purple"]

for color, file in zip(colors, sys.argv[1:]):
    with open(file) as f:
        data = np.array(
            [[float(v) for v in line.strip().split("   ")] for line in f]
        )
    plt.plot(data[:, 0], data[:, 1, color=color)

plt.show()
