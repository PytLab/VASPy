#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bisect import bisect

import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from vaspy.iter import AniFile

lattice_const = [7.70441, 7.70441, 21]
orders = [1, 6, 11, 16]
grid_resolution = 60
interp_resolution = 100

ani = AniFile("OUT.ANI")
trajs = [[]]*len(orders)
for xyz in ani:
    for j in range(len(orders)):
        data = xyz.data[orders[j]]
        new_data = [0]*3
        for i, c in enumerate(data):
            if i == 0 and c >= int(lattice_const[i] - 1):
                c -= lattice_const[i]
            new_data[i] = c
        trajs[j].append(new_data)

# Merge all positions.
positions = np.concatenate(trajs)

def locate(x, y, position):
    i, j = position
    return bisect(x, i)-1, bisect(y, j)-1

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")

    z = np.zeros([grid_resolution, grid_resolution])
    x = np.linspace(-2, 7, grid_resolution)
    y = np.linspace(-2, 7, grid_resolution)
    for xi, yi, zi in positions:
        m, n = locate(x, y, [xi, yi])
        z[m, n] += 1

    # interpolation.
    interp_func = interp2d(x, y, z, kind="linear")

    newx = np.linspace(-2, 7, interp_resolution)
    newy = np.linspace(-2, 7, interp_resolution)
    newz = interp_func(newx, newy)

#    z /= len(positions)
#    x, y = np.meshgrid(x, y)

    CS = plt.contourf(newx, newy, newz, 30, cmap=plt.cm.coolwarm)

    plt.show()

