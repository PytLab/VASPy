# -*- coding:utf-8 -*-
'''
Unit tests for vaspy.functions module.
'''

import unittest
import numpy as np

from ..functions import (str2list, line2list, array2str,
                         combine_atomco_dict, atomdict2str,
                         get_combinations, get_angle)


class Str2listTest(unittest.TestCase):

    def test_str2list(self):
        result = str2list(' 1.0  2.0  3.0 ')
        self.assertListEqual(result, ['1.0', '2.0', '3.0'])

    def test_str2list_empty(self):
        result = str2list('')
        self.assertEqual(result, [])


class Line2listTest(unittest.TestCase):

    def test_line2list_float(self):
        result = line2list('1.0 2.0 3.0', dtype=float)
        self.assertListEqual(result, [1.0, 2.0, 3.0])

    def test_line2list_int(self):
        result = line2list('10 20 30', dtype=int)
        self.assertListEqual(result, [10, 20, 30])

    def test_line2list_str(self):
        result = line2list('a b c', dtype=str)
        self.assertListEqual(result, ['a', 'b', 'c'])

    def test_line2list_custom_field(self):
        result = line2list('1.0,2.0,3.0', field=',', dtype=float)
        self.assertListEqual(result, [1.0, 2.0, 3.0])

    def test_line2list_empty_elements(self):
        result = line2list('  1.0   2.0  ', dtype=float)
        self.assertListEqual(result, [1.0, 2.0])

    def test_line2list_type_error(self):
        with self.assertRaises(TypeError):
            line2list('1.0 2.0', dtype=3.14)


class Array2strTest(unittest.TestCase):

    def test_array2str(self):
        arr = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        result = array2str(arr)
        self.assertIn('1.0000000000000000', result)
        self.assertIn('2.0000000000000000', result)
        self.assertEqual(result.count('\n'), 2)


class CombineAtomcoDictTest(unittest.TestCase):

    def test_combine_disjoint(self):
        a = {'C': [[1.0, 2.0, 3.0]]}
        b = {'O': [[4.0, 5.0, 6.0]]}
        result = combine_atomco_dict(a, b)
        self.assertEqual(set(result.keys()), {'C', 'O'})

    def test_combine_overlap(self):
        a = {'C': [[1.0, 2.0, 3.0]]}
        b = {'C': [[4.0, 5.0, 6.0]]}
        result = combine_atomco_dict(a, b)
        self.assertEqual(len(result['C']), 2)

    def test_combine_empty(self):
        result = combine_atomco_dict({}, {})
        self.assertEqual(result, {})


class Atomdict2strTest(unittest.TestCase):

    def test_atomdict2str(self):
        d = {'C': [[2.01115823704755, 2.33265069974919, 10.54948252493041]],
             'Co': [[0.28355818414485, 2.31976779057375, 2.34330019781397],
                    [2.76900337448991, 0.88479534087197, 2.34330019781397]]}
        result = atomdict2str(d, ['C', 'Co'])
        self.assertIn('C', result)
        self.assertIn('Co', result)
        self.assertEqual(result.count('\n'), 3)


class GetCombinationsTest(unittest.TestCase):

    def test_get_combinations(self):
        result = get_combinations(3, 4, 5)
        self.assertIsInstance(result, np.ndarray)


class GetAngleTest(unittest.TestCase):

    def test_get_angle_90(self):
        v1 = np.array([1.0, 0.0, 0.0])
        v2 = np.array([0.0, 1.0, 0.0])
        self.assertAlmostEqual(get_angle(v1, v2), 90.0)

    def test_get_angle_0(self):
        v1 = np.array([1.0, 0.0, 0.0])
        self.assertAlmostEqual(get_angle(v1, v1), 0.0)

    def test_get_angle_180(self):
        v1 = np.array([1.0, 0.0, 0.0])
        v2 = np.array([-1.0, 0.0, 0.0])
        self.assertAlmostEqual(get_angle(v1, v2), 180.0)
