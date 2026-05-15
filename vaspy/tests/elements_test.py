# -*- coding:utf-8 -*-
'''
Unit tests for vaspy.elements module.
'''

import unittest

from .. import elements


class ElementsTest(unittest.TestCase):

    def test_C12(self):
        self.assertAlmostEqual(elements.C12, 1.99264648e-26)

    def test_amu(self):
        self.assertAlmostEqual(elements.amu, 1.66053904e-27)

    def test_chem_elements_has_H(self):
        self.assertIn('H', elements.chem_elements)
        self.assertEqual(elements.chem_elements['H']['index'], 1)

    def test_chem_elements_has_Ni(self):
        self.assertIn('Ni', elements.chem_elements)
        self.assertEqual(elements.chem_elements['Ni']['index'], 28)

    def test_chem_elements_count(self):
        self.assertEqual(len(elements.chem_elements), 9)
