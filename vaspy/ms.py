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

from vaspy import VasPy


class XsdFile(VasPy):
    def __init__(self, filename):
        VasPy.__init__(self, filename)

    def load(self):
        # get element tree
        tree = ET.ElementTree(file=self.filename)
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
