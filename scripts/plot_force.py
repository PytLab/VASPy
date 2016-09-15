#!/usr/bin/env python

'''
    Script to plot total force trend.
'''
import sys
import logging

import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

from vaspy.iter import OutCar

outcar = OutCar()
# plot
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
forces = outcar.total_forces
step = range(len(forces))
ax.plot(step, forces, linewidth=5, color='#4F94CD')
ax.set_xlabel(r'$\bf{Step}$')
ax.set_ylabel(r'$\bf{Total Force(eV/Angst)}$')
ax.set_ylim(0.0, max(forces)+0.5)

if len(sys.argv) > 1 and 'movie' in sys.argv[1]:
    ax.plot([], [], linewidth=3, color='#CD6889')  # line below forces
    ax.plot([], [], linewidth=3, color='#668B8B')  # line above forces
    line_below, line_above = ax.lines[1:]

    def init():
        line_below.set_data([], [])
        line_above.set_data([], [])
        return line_below, line_above

    def animate(i):
        logging.info('frame %d', i)
        y_below = np.linspace(0, forces[i], 100)
        x = np.array([1.0*i]*100)
        y_above = np.linspace(forces[i], np.max(forces)+0.5, 100)
        line_below.set_data(x, y_below)
        line_above.set_data(x, y_above)

        return line_below, line_above

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(forces),
                                   interval=1.0/16*1000, blit=True)
    anim.save('max_forces.MP4')

plt.show()  # use plt to avoid window being closed
