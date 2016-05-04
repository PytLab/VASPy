# -*- coding:utf-8 -*-
'''
    InCar单元测试.
'''
import unittest

from vaspy.incar import InCar

class InCarTest(unittest.TestCase):

    def setUp(self):
        # Create an InCar object.
        self.incar = InCar("./testdata/INCAR")

    def test_rdata(self):
        " Test data line in INCAR can be read correctly. "

        # Test integer parameter.
        ref_line = "ISTART = 0        # 0 = new job, 1 = restart"
        pnames, datas = self.incar.rdata(ref_line)
        self.assertListEqual(pnames, ["ISTART"])
        self.assertListEqual(datas, ["0"])

        # Test string parameter.
        ref_line = "PREC   = Normal  # [Low/Medium/High/Accurate/Normal]"
        pnames, datas = self.incar.rdata(ref_line)
        self.assertListEqual(pnames, ["PREC"])
        self.assertListEqual(datas, ["Normal"])
        
        # Test comment line.
        ref_line = "! Electronic Structure"
        result = self.incar.rdata(ref_line)
        self.assertIsNone(result)

        # Test multi-parameter line.
        ref_line = "LHFCALC = .TRUE. ; HFSCREEN = 0.2  # HSE"
        pnames, datas = self.incar.rdata(ref_line)
        self.assertListEqual(pnames, ["LHFCALC", "HFSCREEN"])
        self.assertListEqual(datas, [".TRUE.", "0.2"])

    def test_load(self):
        " Test all data in INCAR can be loaded. "
        ref_pnames = ['SYSTEM', 'ISTART', 'ISPIN', 'PREC', 'ENCUT',
                      'NELM', 'NELMIN', 'ISMEAR', 'SIGMA', 'LREAL',
                      'EDIFFG', 'ALGO', 'ISIF', 'NSW', 'IBRION', 'POTIM',
                      'ISYM', 'NWRITE', 'LCHARG', 'LWAVE', 'NCORE']

        ref_datas = ['per', '0', '2', 'Normal', '450', '400', '3',
                     '1', '0.1', 'A', '-0.05', 'Fast', '2', '900',
                     '1', '0.2', '0', '1', '.False.', '.False.', '4']

        for pname, data in zip(ref_pnames, ref_datas):
            self.assertEqual(getattr(self.incar, pname), data)

    def test_parameter_set(self):
        " Test existed parameter can be set correctly. "
        self.assertTrue(self.incar.ISIF, "2")
        self.incar.set("ISIF", 3)
        self.assertTrue(self.incar.ISIF, "3")

    def test_parameter_add(self):
        " Test new parameter can be added correctly. "
        self.assertFalse(hasattr(self.incar, "TEST_zjshao"))
        self.incar.add("TEST_zjshao", "True")
        self.assertTrue(self.incar.TEST_zjshao, "True")

    def test_tofile(self):
        " Test INCAR content can be write to file. "
        # NEED IMPLEMENTATIN
        pass

if "__main__" == __name__:
    suite = unittest.TestLoader().loadTestsFromTestCase(InCarTest)
    unittest.TextTestRunner(verbosity=2).run(suite) 
