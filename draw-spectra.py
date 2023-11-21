#!/usr/bin/env python3
import sys

import matplotlib.pyplot as plt
import numpy as np

with open(sys.argv[1]) as f:
    data = np.array([[float(x) for x in row.strip().split(" ")] for row in f])

xs = data[:, 0]
ys = data[:, 1]

if len(sys.argv) < 3 or sys.argv[2] != "nolog":
    plt.yscale("log")

plt.plot(xs, ys)
plt.show()
