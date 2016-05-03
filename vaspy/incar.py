# -*- coding:utf-8 -*-
"""
========================================================================
Provide INCAR file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, October 2015
Updated by PytLab <shaozhengjiang@gmail.com>, October 2015
========================================================================

"""
from vaspy import VasPy


class InCar(VasPy):
    def __init__(self, filename='INCAR'):
        """
        Create a INCAR file class.

        Example:

        >>> a = InCar()

        Class attributes descriptions
        =======================================================
          Attribute      Description
          ============  =======================================
          filename       string, name of INCAR file
          ============  =======================================
        """
        VasPy.__init__(self, filename)
        self.load()

    def load(self):
        "Load all data in INCAR."
        tot_pnames, tot_datas = [], []
        with open(self.filename, 'r') as f:
            for line in f:
                matched = self.rdata(line)
                if matched:
                    pnames, datas = matched
                    tot_pnames.extend(pnames)
                    tot_datas.extend(datas)
        # set attrs
        for pname, data in zip(tot_pnames, tot_datas):
            setattr(self, pname, data)
        self.pnames = tot_pnames

        return

    @staticmethod
    def rdata(line):
        "Get INCAR data(s) in a line."
        line = line.strip()
        if not line or line.startswith(('!', '#')):
            return None
        else:
            if '#' in line:
                line = line.split('#')[0].strip()
                if '!' in line:
                    line = line.split('!')[0].strip()
            elif '!' in line:
                line = line.split('!')[0].strip()
            # get parameter name and data
            if ';' in line:
                params = [param.strip() for param in line.split(';')]
            else:
                params = [line]
            pnames, datas = [], []
            for param in params:
                pname, data = [i.strip() for i in param.split('=')]
                pnames.append(pname)
                datas.append(data)

            return pnames, datas

    def set(self, pname, data):
        """
        Set a named property of InCar object.

        Example:
        --------
        >>> incar_obj.set("ISIF", 2)
        """
        if not hasattr(self, pname):
            raise ValueError('%s is not in INCAR, ' +
                             'Use add() instead.' % pname)
        setattr(self, pname, str(data))
        return

    def add(self, pname, data):
        """
        Add a new property name to InCar object.

        Example:
        --------
        >>> incar_obj.add("ISIF", 2)
        """
        data = str(data)
        if hasattr(self, pname):
            print ("Waring: %s is already in INCAR, " +
                   "set to %s" % (pname, data))
        else:
            self.pnames.append(pname)
        setattr(self, pname, data)

        return

    def tofile(self):
        "Create INCAR file."
        content = '# Created by VASPy\n'
        for pname in self.pnames:
            if not hasattr(self, pname):
                raise ValueError('Unknown parameter: %s' % pname)
            data = str(getattr(self, pname))
            content += '%s = %s\n' % (pname, data)
        with open('INCAR', 'w') as f:
            f.write(content)

        return
