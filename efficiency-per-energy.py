#!/usr/bin/env python3
import gzip
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np
import uncertainties.unumpy as unp

with gzip.open(sys.argv[1], "rb") as f:
    imat = unp.nominal_values(pickle.load(f))

with gzip.open(sys.argv[2], "rb") as f:
    mat = unp.nominal_values(pickle.load(f))

max_e = float(sys.argv[3:] and sys.argv[3] or "2")

nbins = imat.shape[0]
xs = (np.arange(nbins) + 1 / 2) * max_e / nbins

plt.plot(xs, [mat[x, x] for x in range(nbins)], label="measured")
plt.plot(
    xs, [np.dot(imat[x], mat[:, x]) for x in range(nbins)], label="corrected"
)

plt.xlabel("MeV")

plt.legend()
plt.show()
