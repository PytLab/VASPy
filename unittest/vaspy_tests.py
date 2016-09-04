# -*- coding:utf-8 -*-

import unittest

from incar_test import InCarTest
from outcar_test import OutCarTest
from oszicar_test import OsziCarTest
from xsd_test import XsdTest


def suite():
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(OsziCarTest),
        unittest.TestLoader().loadTestsFromTestCase(OutCarTest),
        unittest.TestLoader().loadTestsFromTestCase(XsdTest),
        unittest.TestLoader().loadTestsFromTestCase(InCarTest)])
    
    return suite

if "__main__" == __name__:
    unittest.TextTestRunner(verbosity=2).run(suite())

