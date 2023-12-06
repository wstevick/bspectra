#!/usr/bin/env python3
import gzip
import pickle
import sys

import numpy as np
import pygame
import uncertainties.unumpy as unp

# values below this will be clamped to MIN_V so they can be logged
MIN_V = 1e-4


with gzip.open(
    sys.stdin.fileno() if sys.argv[1] == "-" else sys.argv[1], "rb"
) as f:
    matrix = unp.nominal_values(pickle.load(f))

# need to transpose the matrix, because of how pygame handles arrays
matrix = matrix.T
# normalize the matrix
matrix /= max(matrix.max(), abs(matrix.min()))

# keep track of where it's negative, for coloring later
negs = (matrix < 0).astype(int)
# take the logarithm and normalize
matrix = 1 - np.log(np.maximum(np.abs(matrix), MIN_V)) / np.log(MIN_V)

# red where the original matrix was negative, green where it was positive
colors = np.zeros((*matrix.shape, 3))
colors[:, :, 0] = matrix * negs
colors[:, :, 1] = matrix * (1 - negs)

# pygame uses a 0-255 scale
colors *= 255

# create a screen with the dimensions of the matrix, then use the color function to put the matrix on the screen
screen = pygame.display.set_mode(matrix.shape)
pygame.surfarray.blit_array(screen, colors)

# save the image to a file for further use
pygame.image.save(screen, "matrix.png")

# traditional pygame event loop. Waits until users hits "close", then exits
while True:
    if any(event.type == pygame.QUIT for event in pygame.event.get()):
        pygame.quit()
        break
    pygame.display.update()
