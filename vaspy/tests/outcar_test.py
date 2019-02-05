# -*- coding:utf-8 -*-
"""
OutCar类单元测试.
"""

import inspect
import os
import unittest

import numpy as np
import matplotlib
matplotlib.use('Agg')

from ..atomco import PosCar
from ..iter import OutCar

from . import path


class OutCarTest(unittest.TestCase):

    def setUp(self):
        #create an instance of OSZICAR file
        self.maxDiff = True

    def test_construction_query(self):
        " Test OutCar construction and query functions. "
        filename = path + "/OUTCAR"
        poscar = path + "/POSCAR"
        outcar = OutCar(filename=filename, poscar=poscar)

        # Check query functions.
        self.assertEqual(outcar.filename, filename)
        self.assertTrue(isinstance(outcar.poscar, PosCar))

        # Check lazy property.
        ref_total_forces = [0.24345800000000001,
                            0.16800399999999999,
                            0.103559,
                            0.046233999999999997]
        ret_total_forces = outcar.total_forces
        self.assertListEqual(ref_total_forces, ret_total_forces)

        self.assertEqual(outcar.last_max_force, 0.046233999999999997)
        self.assertEqual(outcar.last_max_atom, 4)

    def test_forces(self):
        " Make sure we can get correct forces data."
        # {{{
        filename = path + "/OUTCAR"
        poscar = path + "/POSCAR"
        outcar = OutCar(filename=filename,
                        poscar=poscar)

        coords, forces = outcar.forces()

        ref_coords = [[1.78441, 0.85618, 2.29204],
                      [0.16369, 0.85618, 4.56647],
                      [0.97405, -0.5474, 0.0],
                      [0.97405, -0.5474, 6.88358],
                      [4.21548, -0.5474, 2.29204],
                      [2.59476, -0.5474, 4.56647],
                      [3.40512, -1.95098, 0.0],
                      [3.40512, -1.95098, 6.88358],
                      [6.64655, -1.95098, 2.29204],
                      [5.02584, -1.95098, 4.56647],
                      [5.83619, -3.35456, 0.0],
                      [5.83619, -3.35456, 6.88358],
                      [1.78441, 3.66334, 2.29204],
                      [0.16369, 3.66334, 4.56647],
                      [0.97405, 2.25976, 0.0],
                      [0.97405, 2.25976, 6.88358],
                      [4.21548, 2.25976, 2.29204],
                      [2.59476, 2.25976, 4.56647],
                      [3.40512, 0.85618, 0.0],
                      [3.40512, 0.85618, 6.88358],
                      [6.64655, 0.85618, 2.29204],
                      [5.02584, 0.85618, 4.56647],
                      [5.83619, -0.5474, 0.0],
                      [5.83619, -0.5474, 6.88358],
                      [1.78441, 6.4705, 2.29204],
                      [0.16369, 6.4705, 4.56647],
                      [0.97405, 5.06692, 0.0],
                      [0.97405, 5.06692, 6.88358],
                      [4.21548, 5.06692, 2.29204],
                      [2.59476, 5.06692, 4.56647],
                      [3.40512, 3.66334, 0.0],
                      [3.40512, 3.66334, 6.88358],
                      [6.64655, 3.66334, 2.29204],
                      [5.02584, 3.66334, 4.56647],
                      [5.83619, 2.25976, 0.0],
                      [5.83619, 2.25976, 6.88358]]

        ref_forces = [[0.0, -0.0, 0.136895],
                      [0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, -0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [-0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, -0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [-0.0, -0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, -0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [0.0, -0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, -0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [-0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, 0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [-0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, -0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [0.0, -0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, 0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [-0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, 0.0, -0.046234],
                      [0.0, -0.0, 0.136895],
                      [0.0, 0.0, 0.008464],
                      [0.0, -0.0, -0.099126],
                      [-0.0, 0.0, -0.046234]]
        ret_coords, ret_forces = outcar.forces()

        self.assertListEqual(ref_coords, ret_coords)
        self.assertListEqual(ref_forces, ret_forces)
        # }}}

    def test_mask_forces(self):
        " Test private helper function __mask_forces()."
        filename = path + "/OUTCAR"
        poscar = path + "/POSCAR"
        outcar = OutCar(filename=filename, poscar=poscar)

        tfs = [["T", "T", "T"],
               ["F", "F", "F"],
               ["F", "T", "F"]]
        forces = [[1.78441, 0.85618, 2.29204],
                  [0.16369, 0.85618, 4.56647],
                  [0.97405, -0.5474, 0.0]]

        ref_masked_forces = [[1.78441, 0.85618, 2.29204],
                             [0.0, 0.0, 0.0],
                             [0.0, -0.5474, 0.0]]
        ret_masked_forces = outcar._OutCar__mask_forces(forces, tfs)

        self.assertListEqual(ref_masked_forces, ret_masked_forces)

    def test_fmax(self):
        " Make sure we can get correct max forces. "
        filename = path + "/OUTCAR"
        poscar = path + "/POSCAR"
        outcar = OutCar(filename=filename, poscar=poscar)

        coords, forces = outcar.forces()
        ret_index, ret_max_force = outcar.fmax(forces)
        ref_index = 4
        ref_max_force = [-0.0, -0.0, -0.046234]

        self.assertEqual(ret_index, ref_index)
        self.assertListEqual(ret_max_force, ref_max_force)

    def test_freq_iterator(self):
        " Make sure we can get correct frequency iterator. "
        filename = path + "/OUTCAR_freq"
        poscar = path + "/POSCAR_freq"
        outcar = OutCar(filename=filename, poscar=poscar)

        ret_freq_dict = next(outcar.ifreq)

        # Check.
        ref_meV = "93.954209"
        ret_meV = ret_freq_dict["meV"]
        self.assertEqual(ref_meV, ret_meV)

        ref_cm = "757.791533"
        ret_cm = ret_freq_dict["cm-1"]
        self.assertEqual(ref_cm, ret_cm)

        ref_THz = "22.718019"
        ret_THz = ret_freq_dict["THz"]
        self.assertEqual(ref_THz, ret_THz)

        ref_PiTHz = "142.741525"
        ret_PiTHz = ret_freq_dict["2PiTHz"]
        self.assertEqual(ref_PiTHz, ret_PiTHz)

        ref_index = "1"
        ret_index = ret_freq_dict["index"]
        self.assertEqual(ref_index, ret_index)

        ref_freq_type = "f"
        ret_freq_type = ret_freq_dict["freq_type"]
        self.assertEqual(ref_freq_type, ret_freq_type)

        ref_coord = (2.795628, 0.856184, 1.196977)
        ret_coord = ret_freq_dict["coordinates"][0]
        self.assertTupleEqual(ref_coord, ret_coord)

        ref_delta = (0.078066, -0.028474, 0.674474)
        ret_delta = ret_freq_dict["deltas"][-1]
        self.assertTupleEqual(ref_delta, ret_delta)

    def test_zpe(self):
        " Make sure we can get correct ZPE. "
        filename = path + "/OUTCAR_freq"
        poscar = path + "/POSCAR_freq"
        outcar = OutCar(filename=filename, poscar=poscar)

        ref_zpe = 0.1117761635
        ret_zpe = outcar.zpe
        self.assertEqual(ref_zpe, ret_zpe)

        # Check OUTCAR without freq info.
        filename = path + "/OUTCAR"
        poscar = path + "/POSCAR"
        outcar = OutCar(filename=filename, poscar=poscar)

        self.assertFalse(hasattr(outcar, "zpe"))

    def test_freq_types(self):
        " Make sure we can get correct frequency types. "
        filename = path + "/OUTCAR_freq"
        poscar = path + "/POSCAR_freq"
        outcar = OutCar(filename=filename, poscar=poscar)

        ref_freq_types = [["f", "f", "f"],
                          ["f", "f", "f/i"]]
        ret_freq_types = outcar.freq_types

        self.assertListEqual(ref_freq_types, ret_freq_types)

