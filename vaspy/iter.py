# -*- coding:utf-8 -*-
"""
========================================================================
Provide iteration-related file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, August 2015
Updated by PytLab <shaozhengjiang@gmail.com>, March 2017
========================================================================

"""
import re
from string import whitespace

import numpy as np
import matplotlib.pyplot as plt

from vaspy import VasPy, PY2
from vaspy import LazyProperty
from vaspy.atomco import PosCar, XyzFile
from vaspy.functions import line2list
# Copy a XdatCar from atomco.
from vaspy.atomco import XdatCar


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

    # 抽取原子受力信息的正则表达式
    # Regular expression for forces information.
    force_regex = re.compile(r"^\s*POSITION\s+TOTAL-FORCE\s*\(eV\/Angst\)\s*$")
    force_info = ("ion_step", "coordinates", "forces")

    # 抽取频率信息的正则表达式
    # Regular expression for frequency information.
    float_regex = r"(\d+\.\d+)"
    freq_regex = (r"^\s*(\d+)\s*(f|f\/i)\s*=\s*" +
                  float_regex + r"\s*THz\s*" +
                  float_regex + r"\s*2PiTHz\s*" +
                  float_regex + r"\s*cm-1\s*" +
                  float_regex + r"\s*meV\s*$")
    freq_regex = re.compile(freq_regex)
    freq_info = ("index", "freq_type", "THz", "2PiTHz",
                 "cm-1", "meV", "coordinates", "deltas")
    title_regex = re.compile(r"\s*X\s*Y\s*Z\s*dx\s*dy\s*dz\s*")

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
          zpe                 float, 零点能
          freq_types          list of str, 频率类型列表
          ===============    ============================================
        """
        VasPy.__init__(self, filename)

        # Get PosCar object.
        self.poscar = PosCar(poscar)

        # Check parameter validity.
        self.__check()

    def __check(self):
        """
        Private helper function to check consistency of POSCAR and OUTCAR.
        """
        # Coordinates in OUTCAR.
        _, coords, _ = next(self.force_iterator)
        coords_outcar = np.array(coords)
        shape_outcar = coords_outcar.shape

        # Coordinates in POSCAR
        coords_poscar = self.poscar.data
        shape_poscar = coords_poscar.shape

        if shape_poscar != shape_outcar:
            msg = "Shape of data in POSCAR({}) and OUTCAR({}) are different."
            msg = msg.format(shape_poscar, shape_outcar)
            raise ValueError(msg)

    @property
    def force_iterator(self):
        """
        返回每个离子步迭代的步数，坐标和每个原子受力信息。
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
        Function to get the max forces vector and atom index.

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
        获取特定离子步的原子受力信息
        Function to get forces info for a specific step.

        Parameters:
        -----------
        step: The step number, int.

        Return:
        -------
        Coordinates and forces for that step.
        """
        for i, coord, forces in self.force_iterator:
            if step != -1 and i == step:
                return coord, forces

        if step == -1:
            return coord, forces
        elif step > i:
            raise ValueError("Illegal step {} (> {})".format(step, i))

    @LazyProperty
    def total_forces(self):
        """
        获取离子步迭代的原子最大受力（合力）列表。
        Function to get max force for every ionic step.
        """
        max_forces = []
        for _, _, forces in self.force_iterator:
            _, fvector = self.fmax(forces)
            max_force = np.linalg.norm(fvector)
            max_forces.append(max_force)

        return max_forces

    @LazyProperty
    def last_forces(self):
        """
        最后离子步所有原子受力矩阵。
        Function to get forces info of last ionic step.
        """
        _, forces = self.forces(-1)
        return forces

    @LazyProperty
    def last_max_force(self):
        """
        最后一步离子步中原子最大受力（合力）。
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
        最后一个离子步受力最大原子的原子序号。
        Function to get atom number with max force
        in the last ionic step.
        """
        atom_number, _ = self.fmax(self.last_forces)
        return atom_number

    @property
    def freq_iterator(self):
        """
        返回频率信息字典的迭代器。
        Return frequency iterator to generating frequency related data.
        """
        with open(self.filename, "r") as f:
            collecting = False

            for line in f:
                freq = self.freq_regex.match(line)
                title = self.title_regex.match(line)
                empty_line = (line.strip(whitespace) == "")

                if freq:
                    freq_data = list(freq.groups())

                # Collect start.
                if title and not collecting:
                    collecting = True
                    coords, deltas = [], []
                # Collect stop.
                elif empty_line and collecting:
                    collecting = False
                    freq_data.append(coords)
                    freq_data.append(deltas)
                    freq_dict = dict(zip(self.freq_info, freq_data))
                    yield freq_dict
                # Collect data.
                elif collecting:
                    x, y, z, dx, dy, dz = line2list(line)
                    coord = (x, y, z)
                    delta = (dx, dy, dz)
                    coords.append(coord)
                    deltas.append(delta)

    def check_freq_exists(func):
        """
        Decorator to check if frequency information exists.
        """
        def wrapper(self):
            try:
                next(self.freq_iterator)
            except StopIteration:
                msg = "'{}' has no attribtue '{}'".format(self.__class__.__name__, "zpe")
                raise AttributeError(msg)
            return func(self)

        return wrapper


    @LazyProperty
    @check_freq_exists
    def zpe(self):
        """
        从OUTCAR的频率信息返回计算的零点能。
        Function to get Zero Point Energy(ZPE) in eV.
        """
        E = [float(freq_dict["meV"])
             for freq_dict in self.freq_iterator if freq_dict["freq_type"] == "f"]

        return sum(E)/2000.0

    @LazyProperty
    @check_freq_exists
    def freq_types(self):
        """
        获取频率类型列表。
        Function to get frequency types.
        """
        freq_types = [freq_dict["freq_type"] for freq_dict in self.freq_iterator]

        # Reshape.
        try:
            freq_types = np.array(freq_types).reshape((-1, 3)).tolist()
        except ValueError:
            raise ValueError("Number of frequency can not be divided by 3.")

        return freq_types


class AniFile(VasPy):
    """ Class for file containing multiple xyz content.
        e.g. *.ANI file for molden animation visualization.

    Example:

    >>> x = MultiXyz(filename="OUT.ANI")
    """
    def __init__(self, filename="OUT.ANI"):
        VasPy.__init__(self, filename)

        # Get the total atom number for data reading.
        with open(self.filename, "r") as f:
            natom = f.readline()

        self.natom = int(natom)

    def __iter__(self):
        """ Make MultiXyz object iterable.
        """
        with open(self.filename, "r") as f:
            content_list = []
            for i, line in enumerate(f):
                if (i + 1) % (self.natom + 2) == 0:
                    content_list.append(line)
                    yield XyzFile(content_list=content_list)
                    content_list = []
                else:
                    content_list.append(line)

