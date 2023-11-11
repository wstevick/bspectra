#!/usr/bin/env python3
import _thread
import os
import json
import queue
import time

import numpy as np

from get_histogram import get_histogram

# main program variables
# these are what you tweak to alter the simulation
MAX_ENERGY = 2
BIN_SIZE = 0.01
NBINS = int(MAX_ENERGY / BIN_SIZE)
# re-calculate BIN_SIZE in case the number given doesn't evenly divide MAX_ENERGY
BIN_SIZE = MAX_ENERGY / NBINS
BIN_OFFSET = BIN_SIZE / 2
NCASE = 1e4

# this is used to facilitate communications between the main and controller threads
q = queue.Queue()

# this is to keep two threads from trying to print at the same time
print_lock = _thread.allocate_lock()

# this is to keep track of when the program is done
finished_jobs = 0
finished_jobs_lock = _thread.allocate_lock()

fname_base = str(round(time.time()))

# this is to store intermediate data as the program runs
intermediate_file = f"intermediate-{fname_base}"
intermediate_file_lock = _thread.allocate_lock()


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
            print("generating histogram for histid =", histid)

        hist_values, errors = get_histogram(
            histid, NCASE, NBINS, MAX_ENERGY, bin_energies=bin_energies
        )

        # save the results of execution to a temperary file
        with intermediate_file_lock:  # noqa: SIM117
            with open(intermediate_file, "a") as f:
                print(histid, end="\t", file=f)
                print(" ".join(map(str, hist_values)), end="\t", file=f)
                print(" ".join(map(str, errors)), file=f)

        with print_lock:
            print("histogram for histid =", histid, "done")

        # mark one job as done
        with finished_jobs_lock:
            finished_jobs += 1


def main():
    print("bins of", BIN_SIZE, "MeV")
    print("intermediate data in", intermediate_file)

    # for testing purposes
    # this is used to make sure that the histogram bins are what we expect them to be
    bin_energies = np.arange(NBINS) * BIN_SIZE + BIN_OFFSET

    # I'm using a producer/consumer model to divide the work between cores
    # I create a thread for each core on the CPU, and all of them start an EGSnrc process
    # when an EGSnrc process finishes, the thread that started it parses the data, saves it, and starts a new one
    # that way there's (almost) always an EGSnrc process running for each CPU core
    for _ in range(os.cpu_count()):
        _thread.start_new_thread(controller_thread, (bin_energies,))

    for histid in range(1, NBINS + 1):
        q.put(histid)

    # wait until all the jobs have been processed
    while True:
        if finished_jobs == NBINS:
            break
        else:
            time.sleep(1)

    # read the data from the intermediate file and json it
    response_matrix = np.empty((NBINS, NBINS), dtype=float)
    response_matrix_error = np.empty((NBINS, NBINS), dtype=float)
    with open(intermediate_file) as f:
        for line in f:
            histid, values, errors = line.strip().split("\t")
            histid = int(histid)
            response_matrix[:, histid - 1] = np.array(
                list(map(float, values.split(" ")))
            )
            response_matrix_error[:, histid - 1] = np.array(
                list(map(float, errors.split(" ")))
            )

    # save the data to a file using json
    savename = f"save-{fname_base}.json"
    with open(savename, "w") as save_file:
        json.dump((response_matrix, response_matrix_error), save_file)
        print("data saved to", repr(savename))


if __name__ == "__main__":
    main()
