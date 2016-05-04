# -*- coding:utf-8 -*-

import unittest

from oszicar_test import OsziCarTest
from incar_test import InCarTest


def suite():
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(OsziCarTest),
        unittest.TestLoader().loadTestsFromTestCase(InCarTest)])
    
    return suite

if "__main__" == __name__:
    unittest.TextTestRunner(verbosity=2).run(suite())

