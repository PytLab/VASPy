# -*- coding:utf-8 -*-
"""
ArcFile类单元测试.
"""

import inspect
import os
import unittest

from vaspy.matstudio import ArcFile

from tests import path


class ArcTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction_query(self):
        " Test ArcFile construction and query function. "
        filename = path + "/00-04.arc" 
        arc = ArcFile(filename)

        # Check query functions.
        self.assertEqual(arc.filename, filename)

        ref_lengths = [7.9398, 7.9398, 17.9398]
        self.assertListEqual(arc.lengths, ref_lengths)

        ref_angles = [90.0, 90.0, 90.0]
        self.assertListEqual(arc.angles, ref_angles)

    def test_coords_iterator(self):
        " Make sure we can get coordinates correctly. "
        filename = path + "/00-04.arc" 
        arc = ArcFile(filename)

        # NEED IMPLEMENTATION.

if "__main__" == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(ArcTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

