# -*- coding:utf-8 -*-
'''
CifFile单元测试
'''

import unittest

from vaspy.atomco import CifFile
from tests import path


class CifFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_construction(self):
        filename = path + '/ceo2-111.cif'
        cif = CifFile(filename)

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(CifFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

