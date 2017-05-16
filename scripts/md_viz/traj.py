#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

from vaspy.iter import AniFile

lattice_const = [7.70441, 7.70441, 21]

ani = AniFile("OUT.ANI")

orders = [1, 6, 11, 16]

trajs = [[], [], [], []]
for xyz in ani:
    for j in range(len(orders)):
        data = xyz.data[orders[j]]
        new_data = [0]*3
        for i, c in enumerate(data):
            if i == 0 and c >= int(lattice_const[i] - 1):
                c -= lattice_const[i]
            new_data[i] = c
        trajs[j].append(new_data)

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect("equal")
    for traj in trajs:
        traj = np.array(traj)
        ax.scatter(traj[:, 0], traj[:, 1], alpha=0.3, facecolor="#93989A", edgecolor="#000000", s=60)

    plt.show()

