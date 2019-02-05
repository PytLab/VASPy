# -*- coding:utf-8 -*-
'''
CifFile单元测试
'''

import unittest

from ..atomco import CifFile
from . import path


class CifFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction(self):
        filename = path + '/ceo2-111.cif'
        cif = CifFile(filename)

