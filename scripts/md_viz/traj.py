#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from vaspy.iter import XdatCar, AniFile

orders = [2, 6, 10, 14, 18, 22, 26, 30, 34]
max_x = 0.7
max_y = 0.8

def get_trajectories():
    xdatcar = XdatCar()
    ani = AniFile()

    trajs = []
    for i in range(len(orders)):
        trajs.append([])

    for xyz in ani:
        coordinates = xyz.data
        for j in range(len(orders)):
            data = coordinates[orders[j]]
            # Convert to direct coordinate.
            direct_data = xdatcar.cart2dir(xdatcar.bases, data).tolist()
            new_data = [0]*3
            for i, c in enumerate(direct_data):
                if (i == 0 and c >= max_x) or (i == 1 and c > max_y):
                    c -= 1.0
                new_data[i] = c

            # Convert direct coordinates to cartesian coordiantes.
            cart_data = xdatcar.dir2cart(xdatcar.bases, new_data)
            trajs[j].append(cart_data.tolist())

    return trajs

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    trajs = get_trajectories()
    for traj in trajs:
        traj = np.array(traj)
#        import ipdb; ipdb.set_trace()
        ax.scatter(traj[:, 0], traj[:, 1],
                   alpha=0.3, s=60,
                   facecolor="#93989A",
                   edgecolor="#000000")

    plt.show()

