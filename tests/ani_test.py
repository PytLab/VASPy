# -*- coding:utf-8 -*-
'''
AniFile单元测试
'''

import unittest

from vaspy.iter import AniFile
from vaspy.atomco import XyzFile
from tests import path


class AniFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True
        self.filename = path + '/OUT.ANI'

    def test_construction(self):
        ani = AniFile(self.filename)

    def test_iterable(self):
        " Make sure the ani object is iterable."
        ani = AniFile(self.filename)
        generator = iter(ani)
        xyz = next(generator)

        self.assertTrue(isinstance(xyz, XyzFile))
        self.assertListEqual(xyz.atom_types, ["Pt", "C", "O"])
        self.assertListEqual(xyz.atom_numbers, [40, 1, 1])

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(AniFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

