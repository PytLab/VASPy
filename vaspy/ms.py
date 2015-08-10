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
        ms_version = root.attrib.get('Version')
        if ms_version:
            self.ms_version = ms_version

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
