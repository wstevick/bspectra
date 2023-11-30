#!/usr/bin/env python3
import _thread
import csv
import gzip
import os
import pickle
import queue
import time

import numpy as np
import uncertainties.unumpy as unp
from uncertainties import ufloat_fromstr

from get_histogram import get_histogram

# main program variables
# these are what you tweak to alter the simulation
MAX_ENERGY = 2
# BIN_SIZE = 0.01
NBINS = 200  # int(MAX_ENERGY / BIN_SIZE)
# re-calculate BIN_SIZE in case the number given doesn't evenly divide MAX_ENERGY
BIN_SIZE = MAX_ENERGY / NBINS
BIN_OFFSET = BIN_SIZE / 2
NCASE = 1e5

# this is used to facilitate communications between the main and controller threads
q = queue.Queue()

# this is to keep two threads from trying to print at the same time
print_lock = _thread.allocate_lock()

# this is to keep track of when the program is done
finished_jobs = 0
finished_jobs_lock = _thread.allocate_lock()

fname_base = str(round(time.time()))

# this is to store intermediate data as the program runs
intermediate_file = f"intermediate-{fname_base}.csv"
intermediate_file_lock = _thread.allocate_lock()


def get_response_matrix_column(
    histid, ncase, total_nbins, max_energy=2, bin_energies=None
):
    return get_histogram(histid, ncase, total_nbins, max_energy, bin_energies=bin_energies) * max_energy/total_nbins / ncase


# one of these will run for every core on the CPU
# these make sure that there's always as many EGSnrc jobs going as cores
# I'm calling them "controller" threads because they control the exteranal EGSnrc processes
def controller_thread(bin_energies=None):
    # run forever
    # this gets killed when the program exit
    global finished_jobs
    while True:
        histid = q.get()

        with print_lock:
            print(f"generating histogram for histid = {histid}")

        histogram = get_response_matrix_column(
            histid, NCASE, NBINS, MAX_ENERGY, bin_energies=bin_energies
        )

        # save the results of execution to a temperary file
        with intermediate_file_lock:  # noqa: SIM117
            with open(intermediate_file, "a", newline="") as f:
                csv.writer(f).writerow([histid, *histogram])

        with print_lock:
            print(f"histogram for histid = {histid} done")

        # mark one job as done
        with finished_jobs_lock:
            finished_jobs += 1


def main():
    print(f"bins of {BIN_SIZE} MeV")
    print(f"intermediate data in {intermediate_file!r}")

    # I'm using a producer/consumer model to divide the work between cores
    # I create a thread for each core on the CPU, and all of them start an EGSnrc process
    # when an EGSnrc process finishes, the thread that started it parses the data, saves it, and starts a new one
    # that way there's (almost) always an EGSnrc process running for each CPU core
    for _ in range(os.cpu_count()):
        _thread.start_new_thread(controller_thread, ())

    for histid in range(1, NBINS + 1):
        q.put(histid)

    # wait until all the jobs have been processed
    while True:
        if finished_jobs == NBINS:
            break
        else:
            time.sleep(1)

    # read the data from the intermediate file and pickle it
    response_matrix = unp.uarray(np.empty((NBINS, NBINS)), 0)
    with open(intermediate_file, newline="") as f:
        for row in csv.reader(f):
            [histid, *histogram] = row
            response_matrix[:, int(histid) - 1] = [
                ufloat_fromstr(x) for x in histogram
            ]

    # save the data to a file using pickle
    savename = f"save-{fname_base}.pickle.gz"
    with gzip.open(savename, "wb") as save_file:
        pickle.dump(response_matrix, save_file)
        print(f"data saved to {savename!r}")


if __name__ == "__main__":
    main()
