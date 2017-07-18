# -*- coding:utf-8 -*-
"""
========================================================================
Provide pure data file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, September 2015
Updated by PytLab <shaozhengjiang@gmail.com>, September 2015
========================================================================

"""
import numpy as np
import matplotlib.pyplot as plt

from vaspy.functions import line2list


class DataPlotter(object):
    def __init__(self, filename, field=' ', dtype=float):
        self.filename = filename
        self.field = field
        self.dtype = dtype
        #load data
        self.load()

    def load(self):
        "Load all data in file into array."
        data = []
        with open(self.filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:  # blank line
                    continue
                if not line[0].isdigit():  # comment line or not
                    if not line.startswith('-'):
                        continue
                    elif not line[1].isdigit() and line[1] != '.':
                        continue
                linedata = line2list(line, field=self.field,
                                     dtype=self.dtype)
                data.append(linedata)
        self.data = np.array(data)

        return data

    def plot2d(self, xcol, ycols):
        "显示特定两列数据"
        '''
        Parameter
        ---------
        xcol: int
            column number of data for x values
        ycols: tuple of int
            column numbers of data for y values
            (start, stop[, step])
        Example:
        >>> a.plot2d(0, (1, 3, 1))
        '''
        x = self.data[:, xcol]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for i in range(*ycols):
            y = self.data[:, i]
            ax.plot(x, y, linewidth=3)

        fig.show()

    def plotall(self):
        "将所有数据一起显示"
        ncols = self.data.shape[1]
        x = self.data[:, 0]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for col in range(1, ncols):
            y = self.data[:, col]
            ax.plot(x, y, linewidth=3)
        fig.show()

