#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bisect import bisect

import numpy as np
from scipy.interpolate import interp2d
from mayavi import mlab

from vaspy.iter import XdatCar

orders = [2, 6, 10, 14, 18, 22, 26, 30, 34]
max_x = 0.7
max_y = 0.7
grid_resolution = 60
interp_resolution = 100

xdatcar = XdatCar()
trajs = [[]]*len(orders)
for item in xdatcar:
    for j in range(len(orders)):
        data = item.coordinates[orders[j]]
        new_data = [0]*3
        for i, c in enumerate(data):
            if (i == 0 and c >= max_x) or (i == 1 and c > max_y):
                c -= 1.0
            new_data[i] = c

        cart_data = xdatcar.dir2cart(xdatcar.bases, new_data)
        trajs[j].append(cart_data.tolist()[0])

# Merge all positions.
positions = np.concatenate(trajs)

def locate(x, y, position):
    i, j = position
    return bisect(x, i)-1, bisect(y, j)-1

if __name__ == "__main__":
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
    z /= len(positions/len(orders))
    interp_func = interp2d(x, y, z, kind="linear")

    newx = np.linspace(left, right, interp_resolution)
    newy = np.linspace(left, right, interp_resolution)
    newz = interp_func(newx, newy)

    newy, newx = np.meshgrid(newx, newy)

    face = mlab.surf(newx, newy, newz, warp_scale=40)
    mlab.axes(xlabel="x", ylabel="y", zlabel="z")
    mlab.outline(face)

    mlab.show()

