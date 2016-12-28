#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from arc_test import ArcTest
from incar_test import InCarTest
from oszicar_test import OsziCarTest
from outcar_test import OutCarTest
from xsd_test import XsdTest
from xtd_test import XtdTest

def suite():
    suite = unittest.TestSuite([
        unittest.TestLoader().loadTestsFromTestCase(ArcTest),
        unittest.TestLoader().loadTestsFromTestCase(InCarTest),
        unittest.TestLoader().loadTestsFromTestCase(OsziCarTest),
        unittest.TestLoader().loadTestsFromTestCase(OutCarTest),
        unittest.TestLoader().loadTestsFromTestCase(XsdTest),
        unittest.TestLoader().loadTestsFromTestCase(XtdTest),
    ])

    return suite

if "__main__" == __name__:
    result = unittest.TextTestRunner(verbosity=2).run(suite())

    if result.errors or result.failures:
        raise ValueError("Get errors and failures.")

