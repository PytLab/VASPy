# -*- coding:utf-8 -*-
'''
XdatCar单元测试
'''

import unittest

from vaspy.iter import XdatCar
from tests import abs_path


class XdatCarTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True
        self.filename = abs_path + '/testdata/XDATCAR'

    def test_construction(self):
        xdatcar = XdatCar(self.filename)

    def test_iterable(self):
        " Make sure the xdatcar object is iterable."
        xdatcar = XdatCar(self.filename)
        generator = iter(xdatcar)
        item = next(generator)

        self.assertEqual(item.step, 1)

        ref_coord = [[ 0.48879659,  0.44702103,  0.44019084],
                     [ 0.26154368,  0.57210582,  0.59668515],
                     [ 0.24597513,  0.43606684,  0.52376893],
                     [ 0.24574759,  0.56815233,  0.44240966],
                     [ 0.50014572,  0.45350806,  0.59636402],
                     [ 0.49367292,  0.60948493,  0.503559  ],
                     [ 0.79700021,  0.50682229,  0.51311363],
                     [ 0.28253148,  0.5235407 ,  0.5177858 ],
                     [ 0.49369403,  0.5136658 ,  0.51609812],
                     [ 0.68726824,  0.50910242,  0.52968761]]
        self.assertListEqual(item.coordinates.tolist(), ref_coord)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(XdatCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

