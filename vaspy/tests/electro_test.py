# -*- coding:utf-8 -*-
'''
Unit tests for vaspy.electro module.
'''

import unittest
import os
import copy

import numpy as np

from ..electro import DosX, ElfCar, ChgCar
from . import path


class DosXTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(path, "DOS_SUM")

    def test_load(self):
        dosx = DosX(self.filename)
        self.assertIsNotNone(dosx.data)
        self.assertGreater(dosx.data.shape[0], 0)

    def test_reset_data(self):
        dosx = DosX(self.filename)
        dosx.reset_data()
        self.assertTrue(np.all(dosx.data[:, 1:] == 0.0))

    def test_add(self):
        dosx1 = DosX(self.filename)
        dosx2 = DosX(self.filename)
        dos_sum = dosx1 + dosx2
        self.assertEqual(dos_sum.filename, "DOS_SUM")

    def test_deepcopy(self):
        dosx = DosX(self.filename)
        dosx_copy = copy.deepcopy(dosx)
        self.assertTrue(np.all(dosx.data == dosx_copy.data))
        self.assertIsNot(dosx.data, dosx_copy.data)

    def test_tofile(self):
        dosx = DosX(self.filename)
        outfile = os.path.join(path, "_test_dos_output.txt")
        try:
            dosx.tofile(filename=outfile)
            self.assertTrue(os.path.exists(outfile))
        finally:
            if os.path.exists(outfile):
                os.remove(outfile)

    def test_get_dband_center(self):
        dosx = DosX(self.filename)
        dbc = dosx.get_dband_center(d_cols=(5, 10))
        self.assertIsNotNone(dbc)
        self.assertEqual(dosx.dband_center, dbc)

    def test_get_dband_center_int_arg(self):
        dosx = DosX(self.filename)
        dbc = dosx.get_dband_center(d_cols=5)
        self.assertIsNotNone(dbc)

    def test_add_mismatched_energy_raises(self):
        dosx1 = DosX(self.filename)
        dosx2 = DosX(self.filename)
        dosx2.data[0, 0] = 999.0
        with self.assertRaises(ValueError):
            dosx1 + dosx2


class ElfCarTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(path, "ELFCAR")

    def test_load(self):
        elf = ElfCar(self.filename)
        self.assertIsNotNone(elf.elf_data)
        self.assertEqual(len(elf.elf_data.shape), 3)
        self.assertIsNotNone(elf.grid)

    def test_expand_data(self):
        elf = ElfCar(self.filename)
        expanded_data, expanded_grid = elf.expand_data(elf.elf_data, elf.grid, (2, 1, 1))
        self.assertEqual(expanded_data.shape[0], elf.elf_data.shape[0] * 2)
        self.assertEqual(expanded_grid[0], elf.grid[0] * 2)

    def test_contour_bad_distance(self):
        elf = ElfCar(self.filename)
        with self.assertRaises(ValueError):
            elf.plot_contour(distance=1.5)

    def test_contour_bad_show_mode(self):
        elf = ElfCar(self.filename)
        with self.assertRaises(ValueError):
            elf.plot_contour(show_mode='bad')

    def test_contour_cut_x(self):
        elf = ElfCar(self.filename)
        elf.plot_contour(axis_cut='x', show_mode='save')

    def test_contour_cut_y(self):
        elf = ElfCar(self.filename)
        elf.plot_contour(axis_cut='y', show_mode='save')

    def test_contour_cut_z(self):
        elf = ElfCar(self.filename)
        elf.plot_contour(axis_cut='z', show_mode='save')


class ChgCarTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(path, "ELFCAR")

    def test_init(self):
        chg = ChgCar(self.filename)
        self.assertIsNotNone(chg.elf_data)
        self.assertIsNotNone(chg.grid)
