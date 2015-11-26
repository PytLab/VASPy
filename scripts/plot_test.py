from plotter import *
import numpy as np
from scipy.interpolate import interp2d
from mayavi import mlab
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt

a = DataPlotter('PLOTCON')

x = a.data[:, 0]
y = a.data[:, 1]
z = a.data[:, 2]

interpfunc = interp2d(x, y, z)

newx = np.linspace(0, np.max(x), 1000)
newy = np.linspace(0, np.max(y), 1000)
newz = interpfunc(newx, newy)

#extent = [np.min(newx), np.max(newx), np.min(newy), np.max(newy)]
#plt.contourf(newx.reshape(-1), newy.reshape(-1), newz, 20, extent=extent)
#plt.colorbar()
#
##3d plot
#fig3d = plt.figure()
#ax3d = fig3d.add_subplot(111, projection='3d')
#ax3d.plot_surface(newx, newy, newz, cmap=plt.cm.RdBu_r)
#
#plt.show()

#mlab
face = mlab.surf(newx, newy, newz, warp_scale=2)
mlab.axes(xlabel='x', ylabel='y', zlabel='z')
mlab.outline(face)

mlab.show()
