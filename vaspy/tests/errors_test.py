# -*- coding:utf-8 -*-
'''
Unit tests for vaspy.errors module.
'''

import unittest

from ..errors import CarfileValueError, UnmatchedDataShape


class CarfileValueErrorTest(unittest.TestCase):

    def test_raise(self):
        with self.assertRaises(CarfileValueError):
            raise CarfileValueError("test error")

    def test_message(self):
        err = CarfileValueError("bad value")
        self.assertEqual(str(err), "bad value")


class UnmatchedDataShapeTest(unittest.TestCase):

    def test_raise(self):
        with self.assertRaises(UnmatchedDataShape):
            raise UnmatchedDataShape("shape mismatch")

    def test_message(self):
        err = UnmatchedDataShape("shape mismatch")
        self.assertEqual(str(err), "shape mismatch")
