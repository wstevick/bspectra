#!/usr/bin/env python3
import colorsys
import math
import pickle
import sys

import numpy as np
import pygame

# this controls how much lower values are scaled up
# for k = log 10, 0.1 becomes 1/2, 0.01 becomes 1/3, 0.001 becomes 1/4, etc.
k = math.log(10)


# input from 0 to 1, output RGB triplet
def get_color(v):
    return np.array(colorsys.hsv_to_rgb(2 / 3 + v / 3, 1, v * 255))


# the same function, but over a matrix
to_color = np.vectorize(get_color, signature="()->(3)")


with open(sys.argv[1], "rb") as f:
    matrix, _ = pickle.load(f)

# need to transpose the matrix, because of how pygame handles arrays
# also, this way the first axis is the histogram id, which is also more convenient
matrix = matrix.T
# normalize the matrix
column_sums = matrix.sum(axis=1)
column_sums[column_sums == 0] = 1
matrix /= column_sums
# scale the matrix to show off low values
# I may experiment with different algorithms for this, in the future
matrix = k / (k - np.log(matrix))

# create a screen with the dimensions of the matrix, then use the color function to put the matrix on the screen
screen = pygame.display.set_mode(matrix.shape)
pygame.surfarray.blit_array(screen, to_color(matrix))

# traditional pygame event loop. Waits until users hits "close", then exits
while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        pygame.quit()
        break
    pygame.display.update()
