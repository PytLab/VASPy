'''
    Script to plot total force trend.
'''
import sys

import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

from vaspy.iter import OutCar

outcar = OutCar()
# plot
fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111)
forces = outcar.total_forces
step = range(forces.shape[0])
ax.plot(step, forces, linewidth=5, color='#4F94CD')
ax.set_xlabel(r'$\bf{Step}$')
ax.set_ylabel(r'$\bf{Total Force(eV/Angst)}$')
ax.set_ylim(0.0, np.max(forces)+0.5)

if len(sys.argv) > 1 and 'movie' in sys.argv[1]:
    line, = ax.plot([], [], linewidth=5, color='#CD6889')

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        y = np.linspace(0, np.max(forces)+0.5, 100)
        x = np.array([1.0*i]*100)
        line.set_data(x, y)
        return line,

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=step-2,
                                   interval=1.0/16*1000, blit=True)
    anim.save('max_forces.MP4')

plt.show()  # use plt to avoid window being closed
