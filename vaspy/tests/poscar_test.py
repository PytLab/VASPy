# -*- coding:utf-8 -*-
'''
PosCar单元测试
'''

import unittest

from ..atomco import PosCar
from . import path


class PosCarTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.filename = path + "/POSCAR"

    def test_get_poscar_content(self):
        " Make sure we can get the correct poscar content. "
        poscar = PosCar(self.filename)

        ref_content = """Created by VASPy\n 1.000000000\n    7.29321435   -4.21073927    0.00000000\n    0.00000000    8.42147853    0.00000000\n   -0.00000000    0.00000000   16.87610843\n   Pt\n   36\nSelective Dynamics\nDirect\n    0.244666665792    0.223999996980    0.135815443038    F    F    F\n    0.022444443570    0.112888885869    0.271630886077    T    T    T\n    0.133555554681    0.001777774758    0.000000000000    F    F    F\n    0.133555554681    0.001777774758    0.407446329115    T    T    T\n    0.577999999126    0.223999996980    0.135815443038    F    F    F\n    0.355777776904    0.112888885869    0.271630886077    T    T    T\n    0.466888888015    0.001777774758    0.000000000000    F    F    F\n    0.466888888015    0.001777774758    0.407446329115    T    T    T\n    0.911333332459    0.223999996980    0.135815443038    F    F    F\n    0.689111110237    0.112888885869    0.271630886077    T    T    T\n    0.800222221348    0.001777774758    0.000000000000    F    F    F\n    0.800222221348    0.001777774758    0.407446329115    T    T    T\n    0.244666665792    0.557333330313    0.135815443038    F    F    F\n    0.022444443570    0.446222219202    0.271630886077    T    T    T\n    0.133555554681    0.335111108091    0.000000000000    F    F    F\n    0.133555554681    0.335111108091    0.407446329115    T    T    T\n    0.577999999126    0.557333330313    0.135815443038    F    F    F\n    0.355777776904    0.446222219202    0.271630886077    T    T    T\n    0.466888888015    0.335111108091    0.000000000000    F    F    F\n    0.466888888015    0.335111108091    0.407446329115    T    T    T\n    0.911333332459    0.557333330313    0.135815443038    F    F    F\n    0.689111110237    0.446222219202    0.271630886077    T    T    T\n    0.800222221348    0.335111108091    0.000000000000    F    F    F\n    0.800222221348    0.335111108091    0.407446329115    T    T    T\n    0.244666665792    0.890666663647    0.135815443038    F    F    F\n    0.022444443570    0.779555552536    0.271630886077    T    T    T\n    0.133555554681    0.668444441424    0.000000000000    F    F    F\n    0.133555554681    0.668444441424    0.407446329115    T    T    T\n    0.577999999126    0.890666663647    0.135815443038    F    F    F\n    0.355777776904    0.779555552536    0.271630886077    T    T    T\n    0.466888888015    0.668444441424    0.000000000000    F    F    F\n    0.466888888015    0.668444441424    0.407446329115    T    T    T\n    0.911333332459    0.890666663647    0.135815443038    F    F    F\n    0.689111110237    0.779555552536    0.271630886077    T    T    T\n    0.800222221348    0.668444441424    0.000000000000    F    F    F\n    0.800222221348    0.668444441424    0.407446329115    T    T    T\n"""

        ret_content = poscar.get_poscar_content()

        self.assertEqual(ref_content, ret_content)

    def test_add_atom(self):
        "Make sure we can add a new atom to current poscar. "
        poscar = PosCar(self.filename)
        ori_data = poscar.data
        ori_tf = poscar.tf

        poscar.add_atom('O', [0.5, 0.5, 0.5])

        self.assertListEqual(poscar.atom_types, ['Pt', 'O'])
        self.assertListEqual(poscar.atom_numbers, [36, 1])
        self.assertListEqual(ori_data.tolist() + [[0.5, 0.5, 0.5]],
                             poscar.data.tolist())
        self.assertListEqual(ori_tf.tolist() + [['T', 'T', 'T']],
                             poscar.tf.tolist())

