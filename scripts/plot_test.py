from plotter import *
import numpy as np
from scipy.interpolate import interp2d
import pyvista as pv
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

# PyVista surface plot
nx, ny = len(newx), len(newy)
X, Y = np.meshgrid(newx, newy, indexing='ij')
Z = newz.T
surface = pv.StructuredGrid(X[:, :, None], Y[:, :, None], Z[:, :, None])
surface.point_data['scalars'] = Z[:, :, None].flatten(order='F')

pl = pv.Plotter()
pl.add_mesh(surface, scalars='scalars', cmap='viridis', show_scalar_bar=True)
pl.add_axes(xlabel='x', ylabel='y', zlabel='z')
pl.show()
