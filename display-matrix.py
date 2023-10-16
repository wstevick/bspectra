#!/usr/bin/env python3
import colorsys
import math
import pickle
import sys

import numpy as np
import pygame

k = math.log10(10)


# input from 0 to 1, output RGB triplet
def get_color(v):
    return np.array(colorsys.hsv_to_rgb(2 / 3 + v / 3, 1, v * 255))


# the same function, but over a matrix
to_color = np.vectorize(get_color, signature="()->(3)")


with open(sys.argv[1], "rb") as f:
    matrix, errors = pickle.load(f)

# need to transpose the matricies, because of how pygame handles arrays
# also, this way the first axis is the histogram id, which is also more convienent
matrix = matrix.T
errors = errors.T

# calculate the relative errors, and handle 0/0 situations
zeros = errors == 0
rel_errors = errors / matrix
rel_errors[zeros] = 0
assert np.all(rel_errors != np.nan)

# calculate the maximum nonzero relative error for each experimant
max_rel_error_idxs = np.argmax(rel_errors, axis=1)

# normalize the matrix to the 0-1 range
matrix /= matrix.sum(axis=1)

# for each histogram, add the value with the minimum relative error to all the values
# then, take the log10 and rescale
for idx, max_rel_error_idx in enumerate(max_rel_error_idxs):
    hist = matrix[idx]
    min_value = hist[max_rel_error_idx]
    # print(min_value, end=' ')
    hist += min_value

    hist = np.log10(hist)
    rescale_start = np.log10(min_value)
    rescale_stop = np.log10(1 + min_value)
    hist = (hist - rescale_start) / (rescale_stop - rescale_start)
    matrix[idx] = hist

# create a screen with the dimensions of the matrix, then use the color function to put the matrix on the screen
screen = pygame.display.set_mode(matrix.shape)
pygame.surfarray.blit_array(screen, to_color(matrix))

# traditional pygame event loop. Waits until users hits "close", then exits
while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        pygame.quit()
        break
    pygame.display.update()
