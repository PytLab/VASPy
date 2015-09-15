# -*- coding:utf-8 -*-
"""
========================================================================
Provide electro-related file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, September 2015
Updated by PytLab <shaozhengjiang@gmail.com>, September 2015
========================================================================

"""
import copy
from string import whitespace

import numpy as np
from scipy.integrate import simps
from scipy.interpolate import interp2d
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
#whether mayavi installed
try:
    from mayavi import mlab
    mayavi_installed = True
except ImportError:
    mayavi_installed = False

from plotter import DataPlotter
from atomco import PosCar
from functions import line2list


class DosX(DataPlotter):
    def __init__(self, filename, field=' ', dtype=float):
        """
        Create a DOS file class.

        Example:

        >>> a = DosX(filename='DOS1')

        Class attributes descriptions
        =======================================================
          Attribute      Description
          ============  =======================================
          filename       string, name of the SPLITED DOS file
          field          string, separator of a line
          dtype          type, convertion type of data

          reset_data     method, reset object data
          plotsum        method, 绘制多列加合的图像
          ============  =======================================
        """
        DataPlotter.__init__(self, filename=filename, field=' ', dtype=float)

    def __add__(self, dosx_inst):
        sum_dosx = copy.deepcopy(self)
        #相加之前判断能量分布是否相同
        same = (self.data[:, 0] == dosx_inst.data[:, 0]).all()
        if not same:
            raise ValueError('Energy is different.')
        sum_dosx.data[:, 1:] = self.data[:, 1:] + dosx_inst.data[:, 1:]
        sum_dosx.filename = 'DOS_SUM'

        return sum_dosx

    def reset_data(self):
        "Reset data array to zeros."
        self.data[:, 1:] = 0.0

    def plotsum(self, xcol, ycols):
        '''
        绘制多列加合的图像.

        Parameter
        ---------
        xcol: int
            column number of data for x values
        ycols: tuple of int
            column numbers of data for y values
            (start, stop[, step])
        Example:
        >>> a.plotsum(0, (1, 3))
        >>> a.plotsum(0, (5, 10, 2))
        '''
        x = self.data[:, xcol]
        if len(ycols) == 2:
            start, stop = ycols
            step = 1
        else:
            start, stop, step = ycols
        ys = self.data[:, start:stop:step]
        y = np.sum(ys, axis=1)
        #Fermi verical line
        ymax = np.max(y)
        xfermi = np.array([0.0]*50)
        yfermi = np.linspace(0, int(ymax+1), 50)
        #plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, linewidth=5, color='#104E8B')
        #plot fermi energy auxiliary line
        ax.plot(xfermi, yfermi, linestyle='dashed', color='#000000')
        ax.set_xlabel(r'$\bf{E - E_F(eV)}$', fontdict={'fontsize': 20})
        ax.set_ylabel(r'$\bf{pDOS(arb. unit)}$', fontdict={'fontsize': 20})
        fig.show()

        return

    def tofile(self):
        "生成文件"
        "DosX object to DOS file."
        ndata = self.data.shape[1]  # data number in a line
        data = self.data.tolist()
        content = ''
        for datalist in data:
            content += ('%12.8f'*ndata + '\n') % tuple(datalist)
        with open(self.filename, 'w') as f:
            f.write(content)

        return

    def get_dband_center(self):
        "Get d-band center of the DosX object."
        #合并d轨道DOS
        if self.data.shape[1] == 10:
            yd = np.sum(self.data[:, 5:10], axis=1)
        #获取feimi能级索引
        for idx, E in enumerate(self.data[:, 0]):
            if E >= 0:
                nfermi = idx
                break
        E = self.data[: nfermi+1, 0]  # negative inf to Fermi
        dos = yd[: nfermi+1]  # y values from negative inf to Fermi
        #use Simpson integration to get d-electron number
        nelectro = simps(dos, E)
        #get total energy of dband
        tot_E = simps(E*dos, E)
        dband_center = tot_E/nelectro
        self.dband_center = dband_center

        return dband_center


class ElfCar(PosCar):
    def __init__(self, filename='ELFCAR'):
        """
        Create a ELFCAR file class.

        Example:

        >>> a = ElfCar()

        Class attributes descriptions
        ==============================================================
          Attribute       Description
          ==============   =============================================
          filename         string, name of the ELFCAR file
          -------------    ame as PosCar ------------
          bases_const      float, lattice bases constant
          bases            np.array, bases of POSCAR
          atoms            list of strings, atom types
          ntot             int, the number of total atom number
          natoms           list of int, same shape with atoms
                           atom number of atoms in atoms
          tf               list of list, T&F info of atoms
          data             np.array, coordinates of atoms, dtype=float64
          -------------    ame as PosCar ------------
          elf_data         3d array
          plot_contour     method, use matplotlib to plot contours
          plot_mcontours   method, use Mayavi.mlab to plot beautiful contour
          plot_contour3d   method, use mayavi.mlab to plot 3d contour
          plot_field       method, plot scalar field for elf data
          ==============  =============================================
        """
        PosCar.__init__(self, filename=filename)

    def load(self):
        "Rewrite load method"
        PosCar.load(self)
        with open(self.filename, 'r') as f:
            for i in xrange(self.totline):
                f.readline()
            #get dimension of 3d array
            grid = f.readline().strip(whitespace)
            empty = not grid  # empty row
            while empty:
                grid = f.readline().strip(whitespace)
                empty = not grid
            x, y, z = line2list(grid, dtype=int)
            #read electron localization function data
            elf_data = []
            for line in f:
                datalist = line2list(line)
                elf_data.extend(datalist)
        #reshape to 3d array
        elf_data = np.array(elf_data).reshape((x, y, z), order='F')
        #set attrs
        self.grid = x, y, z
        self.elf_data = elf_data

        return

    def plot_contour(self, axis_cut='z', distance=0.5, show_mode='show'):
        '''
        绘制ELF等值线图
        Parameter
        ---------
        axis_cut: str
            ['x', 'X', 'y', 'Y', 'z', 'Z'], axis which will be cut.
        distance: float
            (0.0 ~ 1.0), distance to origin
        show_mode: str
            'save' or 'show'
        '''
        #cope parameters
        if abs(distance) > 1:
            raise ValueError('Distance must be between 0 and 1.')
        if axis_cut in ['X', 'x']:  # cut vertical to x axis
            nlayer = int(self.grid[0]*distance)
            z = self.elf_data[nlayer, :, :]
            ndim0 = self.grid[1]
            ndim1 = self.grid[2]
        elif axis_cut in ['Y', 'y']:
            nlayer = int(self.grid[1]*distance)
            z = self.elf_data[:, nlayer, :]
            ndim0 = self.grid[0]
            ndim1 = self.grid[2]
        elif axis_cut in ['Z', 'z']:
            nlayer = int(self.grid[2]*distance)
            z = self.elf_data[:, :, nlayer]
            ndim0 = self.grid[0]
            ndim1 = self.grid[1]

        #do 2d interpolation
        #get slice object
        s = np.s_[0:ndim0:1, 0:ndim1:1]
        x, y = np.ogrid[s]
        mx, my = np.mgrid[s]
        #use cubic 2d interpolation
        interpfunc = interp2d(x, y, z, kind='cubic')
        newx = np.linspace(0, ndim0, 600)
        newy = np.linspace(0, ndim1, 600)
        #-----------for plot3d---------------------
        ms = np.s_[0:ndim0:600j, 0:ndim1:600j]  # |
        newmx, newmy = np.mgrid[ms]             # |
        #-----------for plot3d---------------------
        newz = interpfunc(newx, newy)

        #plot 2d contour map
        fig2d = plt.figure(figsize=(17, 7))
        ax1 = fig2d.add_subplot(1, 2, 1)
        extent = [np.min(newx), np.max(newx), np.min(newy), np.max(newy)]
        ax1.imshow(newz, extent=extent, origin='lower')
        #plt.colorbar()
        #coutour plot
        ax2 = fig2d.add_subplot(1, 2, 2)
        cs = ax2.contour(newz, 10, extent=extent)
        ax2.clabel(cs)
        #3d plot
        fig3d = plt.figure(figsize=(12, 8))
        ax3d = fig3d.add_subplot(111, projection='3d')
        ax3d.plot_surface(newmx, newmy, newz, cmap=plt.cm.RdBu_r)
        #save or show
        if show_mode == 'show':
            plt.show()
        elif show_mode == 'save':
            fig2d.savefig('contour2d.png', dpi=500)
            fig3d.savefig('surface3d.png', dpi=500)
        else:
            raise ValueError('Unrecognized show mode parameter : ' +
                             show_mode)

        return

    def plot_mcontour(self, axis_cut='z', distance=0.5, show_mode='show'):
        "use mayavi.mlab to plot contour."
        if not mayavi_installed:
            print "Mayavi is not installed on your device."
            return
        #cope parameters
        if abs(distance) > 1:
            raise ValueError('Distance must be between 0 and 1.')
        if axis_cut in ['X', 'x']:  # cut vertical to x axis
            nlayer = int(self.grid[0]*distance)
            z = self.elf_data[nlayer, :, :]
            ndim0 = self.grid[1]
            ndim1 = self.grid[2]
        elif axis_cut in ['Y', 'y']:
            nlayer = int(self.grid[1]*distance)
            z = self.elf_data[:, nlayer, :]
            ndim0 = self.grid[0]
            ndim1 = self.grid[2]
        elif axis_cut in ['Z', 'z']:
            nlayer = int(self.grid[2]*distance)
            z = self.elf_data[:, :, nlayer]
            ndim0 = self.grid[0]
            ndim1 = self.grid[1]

        #do 2d interpolation
        #get slice object
        s = np.s_[0:ndim0:1, 0:ndim1:1]
        x, y = np.ogrid[s]
        mx, my = np.mgrid[s]
        #use cubic 2d interpolation
        interpfunc = interp2d(x, y, z, kind='cubic')
        newx = np.linspace(0, ndim0, 600)
        newy = np.linspace(0, ndim1, 600)
        newz = interpfunc(newx, newy)
        #mlab
        face = mlab.surf(newx, newy, newz, warp_scale=2)
        mlab.axes(xlabel='x', ylabel='y', zlabel='z')
        mlab.outline(face)
        #save or show
        if show_mode == 'show':
            mlab.show()
        elif show_mode == 'save':
            mlab.savefig('mlab_contour3d.png')
        else:
            raise ValueError('Unrecognized show mode parameter : ' +
                             show_mode)

        return

    def plot_contour3d(self, **kwargs):
        '''
        use mayavi.mlab to plot 3d contour.

        Parameter
        ---------
        kwargs: {
            'maxct'   : float, max contour number,
            'nct'     : int, number of contours,
            'opacity' : float, opacity of contour,
        }
        '''
        if not mayavi_installed:
            print "Mayavi is not installed on your device."
            return
        #set parameters
        maxdata = np.max(self.elf_data)
        maxct = kwargs['maxct'] if 'maxct' in kwargs else maxdata
        #check maxct
        if maxct > maxdata:
            print "maxct is larger than %f" % maxdata
        opacity = kwargs['opacity'] if 'opacity' in kwargs else 0.6
        nct = kwargs['nct'] if 'nct' in kwargs else 5
        #plot surface
        surface = mlab.contour3d(self.elf_data)
        #set surface attrs
        surface.actor.property.opacity = opacity
        surface.contour.maximum_contour = maxct
        surface.contour.number_of_contours = nct
        mlab.axes(xlabel='x', ylabel='y', zlabel='z')
        mlab.outline()
        mlab.show()

        return

    def plot_field(self, vmin=0.0, vmax=1.0, axis_cut='z', nct=5):
        "plot scalar field for elf data"
        if not mayavi_installed:
            print "Mayavi is not installed on your device."
            return
        #create pipeline
        field = mlab.pipeline.scalar_field(self.elf_data)  # data source
        mlab.pipeline.volume(field, vmin=vmin, vmax=vmax)  # put data into volumn to visualize
        #cut plane
        if axis_cut in ['Z', 'z']:
            plane_orientation = 'z_axes'
        elif axis_cut in ['Y', 'y']:
            plane_orientation = 'y_axes'
        elif axis_cut in ['X', 'x']:
            plane_orientation = 'x_axes'
        cut = mlab.pipeline.scalar_cut_plane(
            field.children[0], plane_orientation=plane_orientation)
        cut.enable_contours = True  # 开启等值线显示
        cut.contour.number_of_contours = nct
        mlab.show()
        #mlab.savefig('field.png', size=(2000, 2000))

        return
