#!/usr/bin/env python3
import gzip
import pickle
import sys

import numpy as np
from uncertainties.unumpy import nominal_values

with gzip.open(sys.argv[1], "rb") as f:
    mat = pickle.load(f)

mat = nominal_values(mat)

try:
    imat = np.linalg.inv(mat)
except np.linalg.LinAlgError:
    imat = np.linalg.pinv(mat)

ofile = f'{sys.argv[1].removesuffix(".pickle.gz")}-inverted.pickle.gz'
with gzip.open(ofile, "wb") as f:
    pickle.dump(imat, f)
print(f"saved to {ofile!r}")
