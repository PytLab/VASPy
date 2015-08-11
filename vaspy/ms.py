# -*- coding:utf-8 -*-
"""
=============================================================================
Provide Material Studio markup file class which do operations on these files.
=============================================================================
Written by PytLab <shaozhengjiang@gmail.com>, August 2015
Updated by PytLab <shaozhengjiang@gmail.com>, August 2015
==============================================================

"""
import xml.etree.cElementTree as ET

import numpy as np

from atomco import AtomCo
from __init__ import UnmatchedDataShape


class XsdFile(AtomCo):
    def __init__(self, filename):
        """
        Create a Material Studio *.xsd file class.

        Example:

        >>> a = XsdFile(filename='ts.xsd')

        Class attributes descriptions
        =======================================================================
          Attribute      Description
          ============  =======================================================
          filename       string, name of the file the direct coordiante data
                         stored in
          ntot           int, the number of total atom number
          atoms          list of strings, atom types
          natoms         list of tuples, same shape with atoms.
                         (atom name, atom number)
          atoms_num      list of int, atom number of atoms in atoms
          atom_names     list of string,
                         Value of attribute 'Name' in Atom3d tag.
          tf             np.array, T & F info for atoms, dtype=np.string
          data           np.array, coordinates of atoms, dtype=float64
          bases          np.array, basis vectors of space, dtype=np.float64
          ============  =======================================================
        """
        AtomCo.__init__(self, filename)
        self.load()

    def load(self):
        # get element tree
        tree = ET.ElementTree(file=self.filename)
        self.tree = tree
        # MS version info
        root = tree.getroot()
        ms_version = root.get('Version')
        if ms_version:
            self.ms_version = ms_version
        # add WrittenBy attr
        if 'WrittenBy' in root.attrib:
            root.set('WrittenBy', 'VASPy')
        else:
            root.attrib.setdefault('WrittenBy', 'VASPy')

        # atom info
        coordinates = []
        natoms_dict = {}
        atoms = []
        tf = []
        atom_names = []
        for elem in root.iter('Atom3d'):
            if 'XYZ' in elem.attrib:
                # coordinates
                xyz = elem.attrib['XYZ']  # string
                coordinate = [float(i.strip()) for i in xyz.split(',')]
                coordinates.append(coordinate)
                # atom name and number
                atom = elem.attrib['Components']
                if atom not in natoms_dict:
                    natoms_dict.setdefault(atom, 1)
                    atoms.append(atom)
                else:
                    natoms_dict[atom] += 1
                # T&F info
                if 'RestrictedProperties' in elem.attrib:
                    tf.append(['F', 'F', 'F'])
                else:
                    tf.append(['T', 'T', 'T'])
                # atom name
                atom_name = elem.attrib.get('Name')
                atom_names.append(atom_name)
        atoms_num = [natoms_dict[atm] for atm in atoms]
        natoms = zip(atoms, atoms_num)
        # set class attrs
        self.ntot = len(atom_names)
        self.atoms_num = atoms_num
        self.atoms = atoms
        self.natoms = natoms
        self.tf = np.array(tf)
        self.atom_names = atom_names
        self.data = np.array(coordinates)

        # lattice parameters
        bases = []
        for elem in root.iter():
            if elem.tag == 'SpaceGroup':
                for attr in ['AVector', 'BVector', 'CVector']:
                    basis = elem.attrib[attr]  # string
                    basis = [float(i.strip()) for i in basis.split(',')]
                    bases.append(basis)
                break
        self.bases = np.array(bases)

        return

    def update(self):
        "根据最新数据获取更新ElementTree内容"
        if self.ntot != len(self.data):
            raise UnmatchedDataShape('length of data is not equal to atom number.')
        elif self.ntot != len(self.tf):
            raise UnmatchedDataShape('length of tf is not equal to atom number.')
        elif self.ntot != len(self.atom_names):
            raise UnmatchedDataShape('length of atom names is not equal to atom number.')

        idx = 0  # index for atom
        for elem in self.tree.iter('Atom3d'):
            # xyz value
            if 'XYZ' in elem.attrib:
                xyz = self.data[idx, :].tolist()  # list of float
                xyz = ','.join([str(v) for v in xyz])
                elem.set('XYZ', xyz)
                # TF value
                tf = self.tf[idx, :].tolist()
                tf = ','.join(tf)
                if tf == 'F,F,F':
                    if 'RestrictedProperties' not in elem.attrib:
                        elem.attrib.setdefault('RestrictedProperties',
                                               'FractionalXYZ')
                elif tf == 'T,T,T':
                    if 'RestrictedProperties' in elem.attrib:
                        elem.attrib.pop('RestrictedProperties')
                #atom name
                elem.set('Name', self.atom_names[idx])
            idx += 1
        # space group
        bases = self.bases.tolist()
        bases_str = []
        # float -> string
        for basis in bases:
            xyz = ','.join([str(v) for v in basis])  # vector string
            bases_str.append(xyz)
        for elem in self.tree.iter('SpaceGroup'):
            elem.set('AVector', bases_str[0])
            elem.set('BVector', bases_str[1])
            elem.set('CVector', bases_str[2])
            break

        return

    def tofile(self, filename='./new.xsd'):
        "生成文件"
        "XsdFile object to .xsd file."
        self.update()
        self.tree.write(filename)

        return
