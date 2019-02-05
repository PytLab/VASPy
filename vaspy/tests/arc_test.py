# -*- coding:utf-8 -*-
"""
ArcFile类单元测试.
"""

import inspect
import os
import unittest

from ..matstudio import ArcFile

from . import path


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

        for ret_coords in arc.coords_iterator:
            ret_coords = ret_coords.tolist()
            break
        ref_coords = [[0.404932144, 3.164028696, 1.984961526],
                      [0.404932144, 3.164028696, 5.965015241],
                      [0.404932144, 1.17906717, 0.0],
                      [0.404932144, 1.17906717, 3.977019323],
                      [0.404932144, 1.17906717, 7.910692688],
                      [2.38989367, 1.17906717, 1.984961526],
                      [2.38989367, 1.17906717, 5.965015241],
                      [2.38989367, 3.164028696, 0.0],
                      [2.38989367, 3.164028696, 3.977019323],
                      [2.38989367, 3.164028696, 7.910692688],
                      [4.374855196, 3.164028696, 1.984961526],
                      [4.374855196, 3.164028696, 5.965015241],
                      [4.374855196, 1.17906717, 0.0],
                      [4.374855196, 1.17906717, 3.977019323],
                      [4.374855196, 1.17906717, 7.910692688],
                      [6.359816723, 1.17906717, 1.984961526],
                      [6.359816723, 1.17906717, 5.965015241],
                      [6.359816723, 3.164028696, 0.0],
                      [6.359816723, 3.164028696, 3.977019323],
                      [6.359816723, 3.164028696, 7.910692688],
                      [0.404932144, 7.133951749, 1.984961526],
                      [0.404932144, 7.133951749, 5.965015241],
                      [0.404932144, 5.148990222, 0.0],
                      [0.404932144, 5.148990222, 3.977019323],
                      [0.404932144, 5.148990222, 7.910692688],
                      [2.38989367, 5.148990222, 1.984961526],
                      [2.38989367, 5.148990222, 5.965015241],
                      [2.38989367, 7.133951749, 0.0],
                      [2.38989367, 7.133951749, 3.977019323],
                      [2.38989367, 7.133951749, 7.910692688],
                      [4.374855196, 7.133951749, 1.984961526],
                      [4.374855196, 7.133951749, 5.965015241],
                      [4.374855196, 5.148990222, 0.0],
                      [4.374855196, 5.148990222, 3.977019323],
                      [4.374855196, 5.148990222, 7.910692688],
                      [6.359816723, 5.148990222, 1.984961526],
                      [6.359816723, 5.148990222, 5.965015241],
                      [6.359816723, 7.133951749, 0.0],
                      [6.359816723, 7.133951749, 3.977019323],
                      [6.359816723, 7.133951749, 7.910692688],
                      [3.419919646, 4.183439745, 9.201971154]]

        self.assertListEqual(ret_coords, ref_coords)

    def test_elements(self):
        " Test query function elements(). "
        filename = path + "/00-04.arc" 
        arc = ArcFile(filename)

        ref_elements = ['Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt',
                        'Pt', 'Pt', 'Pt', 'Pt', 'Pt', 'O']

        ret_elements = arc.elements

        self.assertListEqual(ref_elements, ret_elements)

