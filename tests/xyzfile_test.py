# -*- coding:utf-8 -*-
'''
XyzFile单元测试
'''

import unittest

from vaspy.atomco import XyzFile
from tests import path


class XyzFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = True

    def test_get_poscar_content(self):
        " Make sure we can get the correct poscar content. "
        filename = path + "/ts.xyz"
        xyz= XyzFile(filename=filename)

        ref_content = """Created by VASPy\n 1.000000000\n    1.00000000    0.00000000    0.00000000\n    0.00000000    1.00000000    0.00000000\n    0.00000000    0.00000000    1.00000000\nH    C    O    Ni   \n    1    1    1   16\nSelective Dynamics\nDirect\n    1.220552640000    1.266963990000    7.889938860000T    T    T    \n    0.609959800000    2.330123250000    8.089289470000T    T    T    \n    0.446344260000    2.754867910000    9.193082960000T    T    T    \n    0.315974300000    0.080747550000    0.195310660000T    T    T    \n    0.315974300000    2.569330200000    0.195310660000T    T    T    \n    2.471150090000   -1.163543780000    0.195310660000T    T    T    \n    2.471150090000    1.325038870000    0.195310660000T    T    T    \n    1.034366230000    1.325038870000    2.227229880000T    T    T    \n    1.034366230000    3.813621520000    2.227229880000T    T    T    \n    3.189542020000    0.080747550000    2.227229880000T    T    T    \n    3.189542020000    2.569330190000    2.227229880000T    T    T    \n    1.749781000000    0.087654860000    4.241213190000T    T    T    \n    3.905934330000   -1.152653240000    4.244935620000T    T    T    \n    1.744802940000    2.577336480000    4.245787570000T    T    T    \n    3.895594450000    1.337641490000    4.262553280000T    T    T    \n    2.432219580000    1.338753760000    6.300456800000T    T    T    \n    0.276629720000    2.610866140000    6.334991110000T    T    T    \n    0.288473570000    0.089652010000    6.252682070000T    T    T    \n    2.452134940000   -1.142741240000    6.231869240000T    T    T    \n"""

        ret_content = xyz.get_poscar_content()

        self.assertEqual(ref_content, ret_content)

    def test_get_xyz_content(self):
        " Make sure we can get correct xyz file content from poscar. "
        filename = path + "/ts.xyz"
        xyz= XyzFile(filename=filename)

        ref_content = """          19\nSTEP =      208\nH        1.22055264      1.26696399      7.88993886\nC         0.6099598      2.33012325      8.08928947\nO        0.44634426      2.75486791      9.19308296\nNi        0.3159743      0.08074755      0.19531066\nNi        0.3159743       2.5693302      0.19531066\nNi       2.47115009     -1.16354378      0.19531066\nNi       2.47115009      1.32503887      0.19531066\nNi       1.03436623      1.32503887      2.22722988\nNi       1.03436623      3.81362152      2.22722988\nNi       3.18954202      0.08074755      2.22722988\nNi       3.18954202      2.56933019      2.22722988\nNi         1.749781      0.08765486      4.24121319\nNi       3.90593433     -1.15265324      4.24493562\nNi       1.74480294      2.57733648      4.24578757\nNi       3.89559445      1.33764149      4.26255328\nNi       2.43221958      1.33875376       6.3004568\nNi       0.27662972      2.61086614      6.33499111\nNi       0.28847357      0.08965201      6.25268207\nNi       2.45213494     -1.14274124      6.23186924\n"""

        ret_content = xyz.get_xyz_content()

        self.assertEqual(ref_content, ret_content)

    def test_construction_from_content(self):
        " Make sure we can construct xyz file object from content string."
        content = """          19\nSTEP =      208\nH        1.22055264      1.26696399      7.88993886\nC         0.6099598      2.33012325      8.08928947\nO        0.44634426      2.75486791      9.19308296\nNi        0.3159743      0.08074755      0.19531066\nNi        0.3159743       2.5693302      0.19531066\nNi       2.47115009     -1.16354378      0.19531066\nNi       2.47115009      1.32503887      0.19531066\nNi       1.03436623      1.32503887      2.22722988\nNi       1.03436623      3.81362152      2.22722988\nNi       3.18954202      0.08074755      2.22722988\nNi       3.18954202      2.56933019      2.22722988\nNi         1.749781      0.08765486      4.24121319\nNi       3.90593433     -1.15265324      4.24493562\nNi       1.74480294      2.57733648      4.24578757\nNi       3.89559445      1.33764149      4.26255328\nNi       2.43221958      1.33875376       6.3004568\nNi       0.27662972      2.61086614      6.33499111\nNi       0.28847357      0.08965201      6.25268207\nNi       2.45213494     -1.14274124      6.23186924\n"""

        xyz = XyzFile(content=content)
        ret_content = xyz.get_xyz_content()
        self.assertEqual(ret_content, content)

    def test_construction_from_content_list(self):
        " Make sure we can construct xyz file object from content list."
        content = """          19\nSTEP =      208\nH        1.22055264      1.26696399      7.88993886\nC         0.6099598      2.33012325      8.08928947\nO        0.44634426      2.75486791      9.19308296\nNi        0.3159743      0.08074755      0.19531066\nNi        0.3159743       2.5693302      0.19531066\nNi       2.47115009     -1.16354378      0.19531066\nNi       2.47115009      1.32503887      0.19531066\nNi       1.03436623      1.32503887      2.22722988\nNi       1.03436623      3.81362152      2.22722988\nNi       3.18954202      0.08074755      2.22722988\nNi       3.18954202      2.56933019      2.22722988\nNi         1.749781      0.08765486      4.24121319\nNi       3.90593433     -1.15265324      4.24493562\nNi       1.74480294      2.57733648      4.24578757\nNi       3.89559445      1.33764149      4.26255328\nNi       2.43221958      1.33875376       6.3004568\nNi       0.27662972      2.61086614      6.33499111\nNi       0.28847357      0.08965201      6.25268207\nNi       2.45213494     -1.14274124      6.23186924"""
        content_list = content.split("\n")

        xyz = XyzFile(content_list=content_list)
        ret_content = xyz.get_xyz_content()
        self.assertEqual(ret_content, content+"\n")

if "__main__" == __name__: 
    suite = unittest.TestLoader().loadTestsFromTestCase(XyzFileTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 

