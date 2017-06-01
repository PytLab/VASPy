#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bisect import bisect

import numpy as np
from scipy.interpolate import interp2d
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from vaspy.iter import XdatCar, AniFile
from traj import get_trajectories

orders = [2, 6, 10, 14, 18, 22, 26, 30, 34]
max_x = 0.7
max_y = 0.7
grid_resolution = 60
interp_resolution = 100


def locate(x, y, position):
    i, j = position
    return bisect(x, i)-1, bisect(y, j)-1

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")

    # Merge all positions.
    trajs = get_trajectories()
    positions = np.concatenate(trajs)

    # Get limits.
    all_data = np.concatenate((positions[:, 0], positions[:, 1]))
    left, right = np.min(all_data), np.max(all_data)

    z = np.zeros([grid_resolution, grid_resolution])
    x = np.linspace(left, right, grid_resolution)
    y = np.linspace(left, right, grid_resolution)
    for xi, yi, zi in positions:
        m, n = locate(x, y, [xi, yi])
        z[m, n] += 1

    # interpolation.
    interp_func = interp2d(x, y, z, kind="linear")

    newx = np.linspace(left, right, interp_resolution)
    newy = np.linspace(left, right, interp_resolution)
    newz = interp_func(newx, newy)

#    z /= len(positions)
#    x, y = np.meshgrid(x, y)

    CS = plt.contourf(newx, newy, newz, 30, cmap=plt.cm.coolwarm)

    plt.show()

