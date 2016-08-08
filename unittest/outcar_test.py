# -*- coding:utf-8 -*-
"""
OutCar类单元测试.
"""

import unittest

import numpy as np
import matplotlib
matplotlib.use('Agg')

from vaspy.atomco import PosCar
from vaspy.iter import OutCar


class OutCarTest(unittest.TestCase):

    def setUp(self):
        #create an instance of OSZICAR file
        self.maxDiff = True

    def test_construction_query(self):
        " Test OutCar construction and query functions. "
        outcar = OutCar(filename="./testdata/OUTCAR",
                        poscar="./testdata/POSCAR")

        # Check query functions.
        self.assertEqual(outcar.filename, "./testdata/OUTCAR")
        self.assertTrue(isinstance(outcar.poscar, PosCar))

    def test_forces(self):
        " Make sure we can get correct forces data."
        # {{{
        outcar = OutCar(filename="./testdata/OUTCAR",
                        poscar="./testdata/POSCAR")
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
        outcar = OutCar(filename="./testdata/OUTCAR",
                        poscar="./testdata/POSCAR")
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
        outcar = OutCar(filename="./testdata/OUTCAR",
                        poscar="./testdata/POSCAR")
        coords, forces = outcar.forces()
        ret_index, ret_max_force = outcar.fmax(forces)
        ref_index = 4
        ref_max_force = [-0.0, -0.0, -0.046234]

        self.assertEqual(ret_index, ref_index)
        self.assertListEqual(ret_max_force, ref_max_force)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OsziCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

