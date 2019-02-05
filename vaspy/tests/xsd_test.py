# -*- coding:utf-8 -*-
"""
XsdFile类单元测试.
"""

import inspect
import os
import unittest
import xml.etree.cElementTree as ET

import numpy as np
import matplotlib
matplotlib.use('Agg')

from ..matstudio import XsdFile

from . import path


class XsdTest(unittest.TestCase):

    def setUp(self):
        #create an instance of OSZICAR file
        self.maxDiff = True

    def test_construction_query(self):
        " Test OutCar construction and query functions. "
        filename = path + "/h_top_c_fcc_far.xsd"
        xsd = XsdFile(filename)

        # Check query functions.
        self.assertEqual(xsd.filename, filename)
        self.assertEqual(xsd.bases_const, 1.0)

        ref_bases = [[  4.31035158,  -2.48858265,   0.        ],
                     [  0.        ,   4.97716529,   0.        ],
                     [  0.        ,   0.        ,  18.09575766]]
        self.assertListEqual(xsd.bases.tolist(), ref_bases)
        self.assertEqual(xsd.force, 0.048)
        self.assertEqual(xsd.energy, -100.896)
        self.assertEqual(xsd.magnetism, 8.25)
        self.assertTrue(hasattr(xsd, "path"))

        # Need other assertions.
        # ...

    def test_get_name_info(self):
        " Make sure we can get correct info from Name property. "
        filename = path + "/h_top_c_fcc_far_noname.xsd"
        xsd = XsdFile(filename)

        self.assertEqual(xsd.force, 0.0)
        self.assertEqual(xsd.energy, 0.0)
        self.assertEqual(xsd.magnetism, 0.0)
        self.assertTrue(hasattr(xsd, "path"))

    def test_update_name(self):
        "Make sure we can update Name info."
        filename = path + "/h_top_c_fcc_far_noname.xsd"
        xsd = XsdFile(filename)

        xsd.update_name()

        for elem in xsd.tree.iter("SymmetrySystem"):
            name = elem.attrib["Name"]
            break

        self.assertTrue("E:" in name)
        self.assertTrue("F:" in name)
        self.assertTrue("M:" in name)
        self.assertTrue("P:" in name)

    def test_bulk_construction(self):
        " Test XsdFile construction for a bulk. "
        filename = path + "/bulk.xsd"
        xsd = XsdFile(filename)

        # Check the default coordinate value for the Atom3d tag without XYZ.
        ref_origin_coord = [0.0, 0.0, 0.0]
        ret_origin_coord = xsd.data[0].tolist()
        self.assertListEqual(ref_origin_coord, ret_origin_coord)

        # Check atom info update in new xsd file.
        temp_file = "{}/temp.xsd".format(path)
        xsd.tofile(temp_file)
        tree = ET.parse(temp_file)
        for atom3d in tree.iter('Atom3d'):
            break
        self.assertEqual(atom3d.get('XYZ'), '0.0,0.0,0.0')
        os.remove(temp_file)

