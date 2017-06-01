# -*- coding:utf-8 -*-
'''
    OsziCar类单元测试.
'''

import os
import unittest

import numpy as np
import matplotlib
matplotlib.use('Agg')

from vaspy.iter import OsziCar

from tests import path


class OsziCarTest(unittest.TestCase):

    def setUp(self):
        #create an instance of OSZICAR file
        self.maxDiff = True

    def test_attrs(self):
        "Make sure load() effects"
        filename = path + "/OSZICAR"
        oszicar = OsziCar(filename) 
        for var in oszicar.vars:
            self.assertTrue(hasattr(oszicar, var))

        #should raise an exception for an AttributeError
        self.assertRaises(AttributeError)

    def test_esort(self):
        "Make sure the esort() effects"
        filename = path + "/OSZICAR"
        oszicar = OsziCar(filename) 
        srted = oszicar.esort('E0', 2)
        shouldbe = np.array([(-101.21186, 326), (-101.21116, 324)],
                            dtype=[('var', '<f8'), ('step', '<i4')])
        #self.assertTrue((srted == shouldbe).all())
        srted = srted.tolist()
        shouldbe = shouldbe.tolist()
        self.assertTrue(srted == shouldbe)

    def test_plot(self):
        "Make sure object could plot"
        filename = path + "/OSZICAR"
        oszicar = OsziCar(filename) 
        plot = oszicar.plot('E0', mode='save')
        self.assertTrue(isinstance(plot, matplotlib.figure.Figure))
        # Remove picture.
        os.remove("E0_vs_step.png")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OsziCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

