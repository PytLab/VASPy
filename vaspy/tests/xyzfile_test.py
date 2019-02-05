# -*- coding:utf-8 -*-
'''
XyzFile单元测试
'''

import unittest

from ..atomco import XyzFile
from . import path


class XyzFileTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_get_poscar_content(self):
        " Make sure we can get the correct poscar content. "
        filename = path + "/ts.xyz"
        xyz= XyzFile(filename=filename)

        ref_content = """Created by VASPy\n 1.000000000\n    1.00000000    0.00000000    0.00000000\n    0.00000000    1.00000000    0.00000000\n    0.00000000    0.00000000    1.00000000\n    H    C    O   Ni\n    1    1    1   16\nSelective Dynamics\nDirect\n    1.220552640000    1.266963990000    7.889938860000    T    T    T\n    0.609959800000    2.330123250000    8.089289470000    T    T    T\n    0.446344260000    2.754867910000    9.193082960000    T    T    T\n    0.315974300000    0.080747550000    0.195310660000    T    T    T\n    0.315974300000    2.569330200000    0.195310660000    T    T    T\n    2.471150090000   -1.163543780000    0.195310660000    T    T    T\n    2.471150090000    1.325038870000    0.195310660000    T    T    T\n    1.034366230000    1.325038870000    2.227229880000    T    T    T\n    1.034366230000    3.813621520000    2.227229880000    T    T    T\n    3.189542020000    0.080747550000    2.227229880000    T    T    T\n    3.189542020000    2.569330190000    2.227229880000    T    T    T\n    1.749781000000    0.087654860000    4.241213190000    T    T    T\n    3.905934330000   -1.152653240000    4.244935620000    T    T    T\n    1.744802940000    2.577336480000    4.245787570000    T    T    T\n    3.895594450000    1.337641490000    4.262553280000    T    T    T\n    2.432219580000    1.338753760000    6.300456800000    T    T    T\n    0.276629720000    2.610866140000    6.334991110000    T    T    T\n    0.288473570000    0.089652010000    6.252682070000    T    T    T\n    2.452134940000   -1.142741240000    6.231869240000    T    T    T\n"""

        ret_content = xyz.get_poscar_content()

        self.assertEqual(ref_content, ret_content)

    def test_get_xyz_content(self):
        " Make sure we can get correct xyz file content from poscar. "
        filename = path + "/ts.xyz"
        xyz= XyzFile(filename=filename)

        ref_content = """          19\nSTEP =      208\nH         1.2205526       1.2669640        7.889939\nC         0.6099598       2.3301233        8.089289\nO         0.4463443       2.7548679        9.193083\nNi        0.3159743       0.0807476       0.1953107\nNi        0.3159743       2.5693302       0.1953107\nNi        2.4711501      -1.1635438       0.1953107\nNi        2.4711501       1.3250389       0.1953107\nNi        1.0343662       1.3250389         2.22723\nNi        1.0343662       3.8136215         2.22723\nNi        3.1895420       0.0807476         2.22723\nNi        3.1895420       2.5693302         2.22723\nNi        1.7497810       0.0876549        4.241213\nNi        3.9059343      -1.1526532        4.244936\nNi        1.7448029       2.5773365        4.245788\nNi        3.8955944       1.3376415        4.262553\nNi        2.4322196       1.3387538        6.300457\nNi        0.2766297       2.6108661        6.334991\nNi        0.2884736       0.0896520        6.252682\nNi        2.4521349      -1.1427412        6.231869\n"""

        ret_content = xyz.get_xyz_content()

        self.assertEqual(ref_content, ret_content)

    def test_construction_from_content(self):
        " Make sure we can construct xyz file object from content string."
        content = """          19\nSTEP =      208\nH         1.2205526       1.2669640        7.889939\nC         0.6099598       2.3301233        8.089289\nO         0.4463443       2.7548679        9.193083\nNi        0.3159743       0.0807476       0.1953107\nNi        0.3159743       2.5693302       0.1953107\nNi        2.4711501      -1.1635438       0.1953107\nNi        2.4711501       1.3250389       0.1953107\nNi        1.0343662       1.3250389         2.22723\nNi        1.0343662       3.8136215         2.22723\nNi        3.1895420       0.0807476         2.22723\nNi        3.1895420       2.5693302         2.22723\nNi        1.7497810       0.0876549        4.241213\nNi        3.9059343      -1.1526532        4.244936\nNi        1.7448029       2.5773365        4.245788\nNi        3.8955944       1.3376415        4.262553\nNi        2.4322196       1.3387538        6.300457\nNi        0.2766297       2.6108661        6.334991\nNi        0.2884736       0.0896520        6.252682\nNi        2.4521349      -1.1427412        6.231869\n"""

        xyz = XyzFile(content=content)
        ret_content = xyz.get_xyz_content()
        self.assertEqual(ret_content, content)

    def test_construction_from_content_list(self):
        " Make sure we can construct xyz file object from content list."
        content = """          19\nSTEP =      208\nH         1.2205526       1.2669640        7.889939\nC         0.6099598       2.3301233        8.089289\nO         0.4463443       2.7548679        9.193083\nNi        0.3159743       0.0807476       0.1953107\nNi        0.3159743       2.5693302       0.1953107\nNi        2.4711501      -1.1635438       0.1953107\nNi        2.4711501       1.3250389       0.1953107\nNi        1.0343662       1.3250389         2.22723\nNi        1.0343662       3.8136215         2.22723\nNi        3.1895420       0.0807476         2.22723\nNi        3.1895420       2.5693302         2.22723\nNi        1.7497810       0.0876549        4.241213\nNi        3.9059343      -1.1526532        4.244936\nNi        1.7448029       2.5773365        4.245788\nNi        3.8955944       1.3376415        4.262553\nNi        2.4322196       1.3387538        6.300457\nNi        0.2766297       2.6108661        6.334991\nNi        0.2884736       0.0896520        6.252682\nNi        2.4521349      -1.1427412        6.231869"""
        content_list = content.split("\n")

        xyz = XyzFile(content_list=content_list)
        ret_content = xyz.get_xyz_content()
        self.assertEqual(ret_content, content+"\n")

