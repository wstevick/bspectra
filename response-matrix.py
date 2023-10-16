#!/usr/bin/env python3
import _thread
import os
import pickle
import queue
import time

import numpy as np

from get_histogram import get_histogram

MAX_ENERGY = 2
NBINS = 8000
NCASE = 1e7
BIN_SIZE = MAX_ENERGY / NBINS
# the offset is because bin positions are given in their *centers*, not the left edges
BIN_OFFSET = BIN_SIZE / 2

# this is used to facilitate communications between the main and controller threads
q = queue.Queue()

# the threads save data here
response_matrix = np.empty((NBINS, NBINS), dtype=float)
response_matrix_error = np.empty((NBINS, NBINS), dtype=float)

print_lock = (
    _thread.allocate_lock()
)  # this is to keep two threads from trying to print at the same time

# this is to keep track of when the program is done
finished_jobs = 0
finished_jobs_lock = _thread.allocate_lock()


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
        # this would cause a race condition, except that two threads will never be writing to the same column of the matrix
        response_matrix[:, histid - 1] = hist_values
        response_matrix_error[:, histid - 1] = errors

        with print_lock:
            print("histogram for histid =", histid, "done")

        # mark one job as done
        with finished_jobs_lock:
            finished_jobs += 1


def main():
    print("bins of", BIN_SIZE, "MeV")

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

    # save the data to a file using pickle
    savename = f"{round(time.time())}.pickle"
    with open(savename, "wb") as save_file:
        pickle.dump((response_matrix, response_matrix_error), save_file)
        print("data saved to", repr(savename))


if __name__ == "__main__":
    main()