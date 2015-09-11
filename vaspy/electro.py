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

import numpy as np
import matplotlib.pyplot as plt

from plotter import DataPlotter


class DosX(DataPlotter):
    def __init__(self, filename, field=' ', dtype=float):
        """
        Create a DOS file class.

        Example:

        >>> a = DataPlotter(filename='DOS1')

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
        #plot
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(x, y, linewidth=3, color='#104E8B')
        ax.set_xlabel('Energy/eV')
        ax.set_ylabel('pDOS(arb. unit)')
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
