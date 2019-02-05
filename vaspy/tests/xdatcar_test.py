# -*- coding:utf-8 -*-
'''
XdatCar单元测试
'''

import unittest

from ..iter import XdatCar
from . import path


class XdatCarTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True
        self.filename = path + '/XDATCAR'

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

    # Test interfaces in AtomCo class.

    def test_cart2dir(self):
        " Make sure we can convert direct coordinates to cartesian coordinates."
        xdatcar = XdatCar(self.filename)
        cart_coord = [1.35366921,  0.95761009,  8.09795]
        dir_coord = xdatcar.cart2dir(xdatcar.bases, cart_coord)
        self.assertListEqual(dir_coord.tolist(), [0.135366921,
                                                  0.09576100900000001,
                                                  0.8097950000000002])

        # Test 2x3 array.
        cart_coord = [[1.35366921,  0.95761009,  8.09795],
                      [1.35366921,  0.95761009,  8.09795]]
        dir_coord = xdatcar.cart2dir(xdatcar.bases, cart_coord)
        ref_coord = [[0.135366921, 0.09576100900000001, 0.8097950000000002],
                     [0.135366921, 0.09576100900000001, 0.8097950000000002]]
        self.assertListEqual(dir_coord.tolist(), ref_coord)

    def test_dir2cart(self):
        " Make sure we can convert cartesian to direct"
        xdatcar = XdatCar(self.filename)
        dir_coord = [0.5, 0.5, 0.5]
        cart_coord = xdatcar.dir2cart(xdatcar.bases, dir_coord).tolist()
        self.assertListEqual(cart_coord, [5.0, 5.0, 5.0])

        dir_coord = [[0.5, 0.5, 0.5], [0.5, 0.5, 0.5]]
        cart_coord = xdatcar.dir2cart(xdatcar.bases, dir_coord).tolist()
        self.assertListEqual(cart_coord, [[5.0, 5.0, 5.0], [5.0, 5.0, 5.0]])

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(XdatCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

