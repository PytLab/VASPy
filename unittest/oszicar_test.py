# -*- coding:utf-8 -*-
'''
    OsziCar类单元测试.
'''
import unittest

import numpy as np

from vaspy.thermo import OsziCar


class TestOsziCar(unittest.TestCase):

    def setUp(self):
        #create an instance of OSZICAR file
        self.x = OsziCar('../testdata/OSZICAR')

    def test_attrs(self):
        "Make sure load() effects"
        for var in self.x.vars:
            self.assertTrue(hasattr(self.x, var))

        #should raise an exception for an AttributeError
        self.assertRaises(AttributeError)

    def test_esort(self):
        "Make sure the esort() effects"
        srted = self.x.esort(2)
        shouldbe = np.array([(-101.21186, 326), (-101.21116, 324)],
                            dtype=[('E0', '<f8'), ('step', '<i4')])
        self.assertTrue((srted == shouldbe).all())

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOsziCar)
    unittest.TextTestRunner(verbosity=2).run(suite)
