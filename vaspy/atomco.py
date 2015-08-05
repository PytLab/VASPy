# -*- coding:utf-8 -*-
"""
===============================================================================================
A XyzFile class which do operations on .xyz files.
===============================================================================================
Written by PytLab <shaozhengjiang@gmail.com>, November 2014
Updated by PytLab <shaozhengjiang@gmail.com>, August 2015

==============================================================

"""
import numpy as np
from functions import *


class CarfileValueError(Exception):
    "Exception raised for errors in the CONTCAR-like file."
    pass


class XyzFile(object):
    """
    Create a OUT.ANI-like file class
    Data begins at 2nd line defaultly
    Example:

    >>> slab_xyz = XyzFile(filename='CONTCAR.xyz', data_begin=2, height=5.5, direction='z')

    Class attributes descriptions
    =======================================================================
      Attribute      Description
      ============  =======================================================
      filename       string, name of the file the direct coordiante data
                     stored in
      data_begin     int, the number of line from which the data begin
      height         float, the slab height
      direction      string, the direction the slab will move in
      contcar        string, CONTCAR templates file name including axes
                     informations
      new_order      boolean, if the instance has a new order of atom,
                     set new_order=True(False default)
      ============  =======================================================
    """
    def __init__(self, filename):
        self.filename = filename
        self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            content_list = f.readlines()
        ntot = int(content_list[0].strip())  # total atom number
        step = int(str2list(content_list[1])[-1])  # iter step number
        data_list = [str2list(line) for line in content_list[2:]]
        #get atom coordinate and number info
        atoms = []
        atomco_dict = {}
        data = []
        for line_list in data_list:
            atom = line_list[0]
            coordinate = line_list[1:]
            data.append(coordinate)
            if atom not in atoms:
                atoms.append(atom)
                atomco_dict.setdefault(atom, [coordinate])
            else:
                atomco_dict[atom].append(coordinate)
        #get atom number for each atom
        atom_num = [len(atomco_dict[k]) for k in atoms]
        natoms = zip(atoms, atom_num)

        #set class attrs
        self.ntot = ntot
        self.step = step
        self.atoms = atoms
        self.natoms = natoms
        self.atomco_dict = atomco_dict
        self.data = np.float64(np.array(data))

        return

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.get_content()

    def coordinate_transfrom(self, axes=np.array([[1.0, 0.0, 0.0],
                                                  [0.0, 1.0, 0.0],
                                                  [0.0, 0.0, 1.0]])):
        "Use Ax=b to do coordinate transform."
        b = np.matrix(self.data.T)
        A = np.matrix(axes).T
        x = A.I*b

        return np.array(x.T)

    def get_content(self):
        ntot = "%12d\n" % self.ntot
        step = "STEP =%9d\n" % self.step
        data = atomdict2str(self.atomco_dict, self.atoms)
        content = ntot + step + data

        return content

    def tofile(self, filename='atomco.xyz'):
        "XyzFile object to .xyz file."
        content = self.get_content()

        with open(filename, 'w') as f:
            f.write(content)

        return


class PosCar(object):
    def __init__(self, filename):
        """
        Class to generate POSCAR or CONTCAR-like objects.
        """
        self.filename = filename
        #load all data in file
        self.load()

    def load(self):
        "Load all information in POSCAR."
        with open(self.filename, 'r') as f:
            content_list = f.readlines()
            #get scale factor
            axes_coeff = float(content_list[1])
            #axes
            axes = [str2list(axis) for axis in content_list[2:5]]
            #atom info
            atoms = str2list(content_list[5])
            natoms = str2list(content_list[6])  # atom number
            #data
            data, tf = [], []  # data and T or F info
            for line_str in content_list[9:]:
                line_list = str2list(line_str)
                data.append(line_list[:3])
                if len(line_list) > 3:
                    tf.append(line_list[3:])
        #data type convertion
        axes = np.float64(np.array(axes))  # to float
        natoms = [int(i) for i in natoms]
        data = np.float64(np.array(data))

        #set class attrs
        self.axes_coeff = axes_coeff
        self.axes = axes
        self.atoms = zip(atoms, natoms)
        self.data = data
        self.tf = tf

        return

    def __repr__(self):
        return self.get_content()

    def __str__(self):
        return self.__repr__()

    def get_content(self):
        content = 'Created by VASPy\n'
        axe_coeff = " %.9f\n" % self.axes_coeff
        #axes
        axes_list = self.axes.tolist()
        axes = ''
        for axis in axes_list:
            axes += "%14.8f%14.8f%14.8f\n" % tuple(axis)
        #atom info
        atoms, natoms = zip(*self.atoms)
        atoms = ("%5s"*len(atoms)+"\n") % atoms
        natoms = ("%5d"*len(natoms)+"\n") % natoms
        #string
        info = "Selective Dynamics\nDirect\n"
        #data and tf
        data_tf = ''
        for data, tf in zip(self.data.tolist(), self.tf):
            data_tf += ("%18.12f"*3+"%5s"*3+"\n") % tuple(data+tf)
        #merge all strings
        content += axe_coeff+axes+atoms+natoms+info+data_tf

        return content

    def tofile(self, filename='POSCAR_c'):
        "PosCar object to POSCAR or CONTCAR."
        content = self.get_content()

        with open(filename, 'w') as f:
            f.write(content)

        return
