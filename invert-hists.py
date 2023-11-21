#!/usr/bin/env python3
import gzip
import pickle
import sys

import uncertainties.unumpy as unp

with gzip.open(sys.argv[1], "rb") as f:
    imat = pickle.load(f)

with gzip.open(sys.argv[2], "rb") as f:
    hdat = pickle.load(f)

hdat["hist_data"] = [
    unp.uarray(unp.nominal_values(imat @ hist), 0)
    for hist in hdat["hist_data"]
]

ofile = f'{sys.argv[2].removesuffix(".pickle.gz")}-inverted.pickle.gz'
with gzip.open(ofile, "wb") as f:
    pickle.dump(hdat, f)
print(f"saved to {ofile!r}")
