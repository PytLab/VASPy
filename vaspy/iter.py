# -*- coding:utf-8 -*-
"""
========================================================================
Provide iteration-related file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, August 2015
Updated by PytLab <shaozhengjiang@gmail.com>, August 2016
========================================================================

"""
import re

import numpy as np
import matplotlib.pyplot as plt

from vaspy import VasPy, PY2
from vaspy import LazyProperty
from vaspy.atomco import PosCar
from vaspy.functions import line2list


class OsziCar(VasPy):
    def __init__(self, filename='OSZICAR'):
        """
        Create a OSZICAR file class.

        Example:

        >>> a = OsziCar(filename='OSZICAR')

        Class attributes descriptions
        =======================================================
          Attribute      Description
          ============  =======================================
          filename       string, name of the SPLITED DOS file
          vars           list of strings, 每次迭代得到的数据
          esort()        method, 对数据进行排序
          plot()         method, 对数据绘图
          ============  =======================================
        """
        super(self.__class__, self).__init__(filename)

        #set regex patterns
        float_regex = r'[\+|-]?\d*\.\d*(?:[e|E][\+|-]?\d+)?'
        eq_regex = r'\s*([\w|\d|\s]+)\=\s*(' + float_regex + r')\s*'
        split_regex = r'^\s*(\d+)\s*((' + eq_regex + r')+)$'  # 将step和其余部分分开

        self.eq_regex = re.compile(eq_regex)
        self.split_regex = re.compile(split_regex)

        self.load()

    def match(self, line):
        "匹配每一步迭代的数据"
        m = self.split_regex.search(line)
        if m:
            # Get step
            step = int(m.group(1))

            # Get other data
            resid = m.group(2)
            eq_tuples = self.eq_regex.findall(resid)  # list of tuples
            if PY2:
                names, numbers = zip(*eq_tuples)
            else:
                names, numbers = list(zip(*eq_tuples))

            # Remove space in names.
            names = [name.replace(' ', '') for name in names]

            #convert string to float
            numbers = [float(number) for number in numbers]
            if PY2:
                eq_tuples = [('step', step)] + zip(names, numbers)
            else:
                eq_tuples = [('step', step)] + list(zip(names, numbers))
            return eq_tuples
        else:
            return None

    def load(self):
        "加载文件数据信息"
        with open(self.filename, 'r') as f:
            content = ''
            for line in f:
                eq_tuples = self.match(line)
                if eq_tuples:  # if matched
                    if not hasattr(self, 'vars'):
                        if PY2:
                            self.vars, numbers = zip(*eq_tuples)
                        else:
                            self.vars, numbers = list(zip(*eq_tuples))

                    for name, number in eq_tuples:
                        if not hasattr(self, name):
                            setattr(self, name, [number])
                        else:
                            getattr(self, name).append(number)
                    content += line
            self.content = content
            #convert list to numpy array
            for var in self.vars:
                data = getattr(self, var)
                setattr(self, var, np.array(data))

        return

    def esort(self, var, n, reverse=False):
        '''
        进行数据var排序, 获取排序后的前n个值.

        Example:
        >>> esort('E0', 10, reverse=True)

        Parameters
        ----------
        var: string, data to be sorted.

        n: int, top numbers of sorted data.

        '''
        if PY2:
            zipped = zip(getattr(self, var), self.step)  # (E0, step)
        else:
            zipped = list(zip(getattr(self, var), self.step))
        dtype = [('var', float), ('step', int)]
        zipped = np.array(zipped, dtype=dtype)
        srted = np.sort(zipped, order='var')

        if reverse:
            return srted[-n:]
        else:
            return srted[:n]

    def plot(self, var, mode='show'):
        "绘制不同变量随step的变化曲线"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylabel(var)
        ax.set_xlabel('step')
        ax.plot(self.step, getattr(self, var), linewidth=2.5)
        if mode == 'show':
            plt.show()
        elif mode == 'save':
            fname = "%s_vs_%s.png" % (var, 'step')
            fig.savefig(fname)
        else:
            raise ValueError('Unrecognized show mode parameter : ' + mode)

        return fig


class OutCar(VasPy):

    force_regex = re.compile(r"^ POSITION\s+TOTAL-FORCE\s*\(eV\/Angst\)$")

    def __init__(self, filename="OUTCAR", poscar="POSCAR"):
        """
        Create a OUTCAR file class.

        Parameters:
        -----------
        filename: File name of OUTCAR, default name is "OUTCAR"(OUTCAR in current path).

        poscar: File name of POSCAR, default value is "POSCAR"(POSCAR in current path).

        Example:

        >>> a = OutCar(filename='OUTCAR', poscar="POSCAR")

        Class attributes descriptions
        =================================================================
          Attribute           Description
          ===============    ============================================
          filename            string, name of OUTCAR file
          max_forces          list of float, 每个离子步迭代的最大原子受力
          last_max_force      float, 最后一步的最大原子受力
          last_max_atom       int, 最后一步受力最大原子序号
          ===============    ============================================
        """
        VasPy.__init__(self, filename)

        # Get PosCar object.
        self.poscar = PosCar(poscar)

    def __iter__(self):
        """
        Return a generator yield ionic_step, coordinates, forces on atoms.

        NOTE: ionic step starts from 1 **NOT 0**.
        """
        with open(self.filename, "r") as f:
            ion_step = 0

            # Force data collection flags.
            collect_begin = False
            collecting = False

            # Collect force data for each ionic step and yield.
            for line in f:
                if not collect_begin:
                    if self.force_regex.match(line):
                        collect_begin = True
                        ion_step += 1
                elif not collecting:
                    if "-"*6 in line:
                        collecting = True
                        coordinates = []
                        forces = []
                else:
                    if "-"*6 in line:
                        collecting = False
                        collect_begin = False
                        yield ion_step, coordinates, forces
                    else:
                        x, y, z, fx, fy, fz = line2list(line)
                        coordinates.append([x, y, z])
                        forces.append([fx, fy, fz])

    def __mask_forces(self, atom_forces, tfs):
        """
        Private helper function to use F/T info to mask forces.

        Returns:
        --------
        Masked forces 2D array.
        """
        # Check atom forces.
        if len(tfs) != len(atom_forces):
            msg = "Length of atom forces({}) must be equal to length of atoms({})."
            msg = msg.format(len(atom_forces), len(tfs))
            raise ValueError(msg)

        masked_forces = []
        for tf_vector, forces in zip(tfs, atom_forces):
            masked_force = []
            for tf, force in zip(tf_vector, forces):
                if tf == "F":
                    masked_force.append(0.0)
                else:
                    masked_force.append(force)
            masked_forces.append(masked_force)

        return masked_forces

    def fmax(self, atom_forces):
        """
        Static method for getting the max forces vector and atom index.

        Parameters:
        -----------
        atom_forces: 2D array of floats, forces on each atom.

        Return:
        -------
        The atom number with max force and force vector.
        NOTE: atom number start from **1 NOT 0**
        """
        # Mask forces.
        masked_forces = self.__mask_forces(atom_forces, self.poscar.tf)

        # Get max forces.
        max_force = max(masked_forces, key=lambda x: sum([i**2 for i in x]))
        index = masked_forces.index(max_force)

        return index + 1, max_force

    def forces(self, step=-1):
        """
        Function to get forces info for a specific step.
        获取特定离子步的原子受力信息

        Parameters:
        -----------
        step: The step number, int.

        Return:
        -------
        Coordinates and forces for that step.
        """
        for i, coord, forces in self.__iter__():
            if step != -1 and i == step:
                return coord, forces

        if step == -1:
            return coord, forces
        elif step > i:
            raise ValueError("Illegal step {} (> {})".format(step, i))

    @LazyProperty
    def total_forces(self):
        """
        Function to get max force for every ionic step.
        """
        max_forces = []
        for _, _, forces in self.__iter__():
            _, fvector = self.fmax(forces)
            max_force = np.linalg.norm(fvector)
            max_forces.append(max_force)

        return max_forces

    @LazyProperty
    def last_forces(self):
        """
        Function to get forces info of last ionic step.
        """
        _, forces = self.forces(-1)
        return forces

    @LazyProperty
    def last_max_force(self):
        """
        Function to get the max force in last ionic step.

        Returns:
        --------
        The max force value of last ionic step.
        """
        _, fvector = self.fmax(self.last_forces)
        f = np.linalg.norm(fvector)

        return f

    @LazyProperty
    def last_max_atom(self):
        """
        Function to get atom number with max force
        in the last ionic step.
        """
        atom_number, _ = self.fmax(self.last_forces)
        return atom_number

