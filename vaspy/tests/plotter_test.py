# -*- coding:utf-8 -*-
'''
Unit tests for vaspy.plotter module.
'''

import unittest
import os

from ..plotter import DataPlotter
from . import path


class DataPlotterTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(path, "PLOTCON")

    def test_load(self):
        plotter = DataPlotter(self.filename)
        self.assertIsNotNone(plotter.data)
        self.assertGreater(plotter.data.shape[0], 0)
        self.assertGreater(plotter.data.shape[1], 0)

    def test_attributes(self):
        plotter = DataPlotter(self.filename)
        self.assertEqual(plotter.filename, self.filename)
        self.assertEqual(plotter.field, ' ')
        self.assertEqual(plotter.dtype, float)
