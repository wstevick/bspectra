import _thread
import glob
import os
import re
import shutil
import subprocess
import time

import numpy as np
import uncertainties.unumpy as unp

MAX_TRIES = 5

# read in the EGS input template code
with open("histogram.egsinp.template") as code_file:
    template_code = code_file.read()

# this regular expression matches the output format for the histogram
# the actual numbers are saved in the first capture group
data_pattern = re.compile(
    "Pulse height distribution in region 1\n======================================================\n((?:\n"
    r"\d+(?:\.\d+)?   \d+(?:\.\d+)?   \d+(?:\.\d+)?)+)"
)

# this is used to give each get_histogram call within a given process a unique filename
# ncalls gets incremented every time get_histogram is called, and the lock is used to make it threadsafe
ncalls = 0
ncalls_lock = _thread.allocate_lock()


def get_histogram(
    histid, ncase, total_nbins, max_energy=2, ntries=0, bin_energies=None
):
    # create a temperary file to hold the generated egsinp code for the given histogram
    global ncalls
    with ncalls_lock:
        ncalls += 1
        # unique filename prefix
        # ncalls is included to make sure that two calls to this function within a process won't share files
        # os.getpid() is included to make sure that two simultanious processes won't share files
        # round(time.time()) is in case two processes that call this happen to share PIDs
        # it ends with a "-" to keep a file at t=13 from interferring with a file at t=1320 (because of the glob)
        # thiat has basically zero probability, but it's a matter of principle
        fname_start = (
            f"delete-me-please{ncalls}-{os.getpid()}-{round(time.time())}-"
        )
    inputfile = f"{fname_start}.egsinp"

    # create egsinp code with template vars set
    # EGSnrc only outputs histograms upto the simulation energy level, so low-energy simulations need fewer bins
    bin_size = max_energy / total_nbins
    energy = histid * bin_size
    code = (
        template_code.replace("TEMPLATE_VAR_NBINS", str(histid))
        .replace("TEMPLATE_VAR_ENERGY", str(energy))
        .replace("TEMPLATE_VAR_NCASE", str(ncase))
        .replace(
            "TEMPLATE_VAR_AE", str(max(0.511 + bin_size, 0.5115667283535004))
        )
        .replace("TEMPLATE_VAR_AP", str(max(bin_size, 0.000999995278993281)))
    )
    try:
        # create temperary egsinp file with the code generated
        with open(inputfile, "w") as f:
            f.write(code)

        # run EGSnrc with the file, and save the results
        proc = subprocess.run(
            ["bspectra", "-i", str(inputfile)],
            capture_output=True,
            check=False,
        )
        output = proc.stdout.decode().replace("\r", "")
    finally:
        # delete all created files, regardless of whether the process works or not
        # sometimes this directory is created. Delete it if it exists
        for dirname in glob.iglob(f"egsrun_*_{fname_start}_*"):
            shutil.rmtree(dirname, ignore_errors=True)
        # delete the input file, and all the files EGSnrc spits out
        for fname in glob.iglob(fname_start + "*"):
            os.remove(fname)

    # parse the process output for distribution heights
    # if, for whatever reason we can't just return zeros
    match = data_pattern.search(output)
    if match is None:
        # if we don't get any data, retry up to five times
        if ntries < MAX_TRIES:
            return get_histogram(
                histid, ncase, total_nbins, max_energy, ntries + 1
            )
        else:
            print(
                f"error running get_histogram({histid}, {ncase}, {total_nbins}, {max_energy})"
            )
            print(output)
            print(proc.stderr.decode())
            return np.zeros(total_nbins), np.zeros(total_nbins)

    data = match.group(1)  # extract only the numbers from the output
    # convert the text table into a numpy array of numbers
    # column 0 is the center of the histogram bin, column 1 in the actual value, and column 2 is the error
    # (I hope)
    data = np.array(
        [
            [float(n) for n in row.split("   ")]
            for row in data.strip().split("\n")
        ]
    )

    # if bin_energies is given, double-check that the histogram energies are what are expected
    # this is for testing purposes only
    if bin_energies is not None:
        assert np.allclose(data[:, 0], bin_energies[:histid])

    # return the histogram values and errors, padded with zeros at the end
    return (
        np.pad(
            unp.uarray(data[:, 1], data[:, 2]),
            (0, total_nbins - histid),
            "constant",
        )
        * ncase
    )
