#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from .arc_test import ArcTest
from .incar_test import InCarTest
from .oszicar_test import OsziCarTest
from .outcar_test import OutCarTest
from .xsd_test import XsdTest
from .xtd_test import XtdTest
from .poscar_test import PosCarTest
from .xyzfile_test import XyzFileTest
from .cif_test import CifFileTest
from .ani_test import AniFileTest
from .xdatcar_test import XdatCarTest
from .functions_test import (Str2listTest, Line2listTest, Array2strTest,
                             CombineAtomcoDictTest, Atomdict2strTest,
                             GetCombinationsTest, GetAngleTest)
from .plotter_test import DataPlotterTest
from .electro_test import DosXTest, ElfCarTest, ChgCarTest
from .elements_test import ElementsTest
from .errors_test import CarfileValueErrorTest, UnmatchedDataShapeTest

if __name__ == '__main__':
    unittest.main()

