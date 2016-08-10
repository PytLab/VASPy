# -*- coding:utf-8 -*-
"""
========================================================================
Provide INCAR file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, October 2015
Updated by PytLab <shaozhengjiang@gmail.com>, July 2016
========================================================================

"""
import logging

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
        super(self.__class__, self).__init__(filename)
        self.filename = filename
        self.load()

        # Set logger.
        self.__logger = logging.getLogger("vaspy.InCar")

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

        # Set parameter names and data lists.
#        sorted_pnames, sorted_datas = self.__sort_two_lists(tot_pnames, tot_datas)
#        self.pnames = sorted_pnames
#        self.datas = sorted_datas
        self.pnames = tot_pnames
        self.datas = tot_datas

        return

    def __sort_two_lists(self, list1, list2):
        """
        Private helper function to sort two lists.
        """
        assert len(list1) == len(list2)

        # Sort the pairs according the entries of list1.
        sorted_pairs = sorted(zip(list1, list2), key=lambda pair: pair[0])
        sorted_list1, sorted_list2 = [list(x) for x in zip(*sorted_pairs)]

        return sorted_list1, sorted_list2

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
        Set a named parameter of InCar object.

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
        Add a new parameter name to InCar object.

        Example:
        --------
        >>> incar_obj.add("ISIF", 2)
        """
        data = str(data)
        if hasattr(self, pname):
            msg = "{} is already in INCAR, set to {}".format(pname, data)
            self.__logger.warning(msg)
        else:
            self.pnames.append(pname)
        setattr(self, pname, data)

        return

    def pop(self, pname):
        """
        Delete a parameter from InCar object.

        Returns:
        --------
        parameter name, parameter value.

        Example:
        --------
        >>> incar_obj.del("ISIF")
        """
        if not hasattr(self, pname):
            msg = "InCar has no parameter '{}'".format(pname)
            self.__logger.warning(msg)
            return

        # Delete from pnames and datas.
        idx = self.pnames.index(pname)
        self.pnames.pop(idx)
        data = self.datas.pop(idx)

        # Delete attribute.
        del self.__dict__[pname]

        return pname, data

    def compare(self, another):
        """
        Function to compare two InCar objects.
        
        Parameters:
        -----------
        another: Another InCar object.

        Returns:
        --------
        A tuple of two dictionaries containing difference informations.
        """
        tot_pnames = set(self.pnames + another.pnames)

        self_dict, another_dict = {}, {}
        for pname in tot_pnames:
            # If both have, check the difference.
            if (pname in self.pnames and pname in another.pnames):
                self_data = getattr(self, pname)
                another_data = getattr(another, pname)
                if self_data != another_data:
                    self_dict.setdefault(pname, self_data)
                    another_dict.setdefault(pname, another_data)
            else:
                # Only in this object.
                if pname in self.pnames:
                    self_data = getattr(self, pname)
                    self_dict.setdefault(pname, self_data)
                    another_dict.setdefault(pname, "")
                # Only in the other object.
                else:
                    another_data = getattr(another, pname)
                    another_dict.setdefault(pname, another_data)
                    self_dict.setdefault(pname, "")

        return self_dict, another_dict

    def __eq__(self, another):
        """
        Overload euqal operator function.
        """
        self_dict, another_dict = self.compare(another)

        if (not self_dict) and (not another_dict):
            return True
        else:
            return False

    def __ne__(self, another):
        """
        Overload not equal operator function.
        """
        if self == another:
            return False
        else:
            return True

    def tofile(self, filename=None):
        "Create INCAR file."
        content = '# Created by VASPy\n'
        for pname in self.pnames:
            if not hasattr(self, pname):
                raise ValueError('Unknown parameter: %s' % pname)
            data = str(getattr(self, pname))
            content += '%s = %s\n' % (pname, data)

        # Write to file.
        if filename is None:
            filename = self.filename
        with open(filename, 'w') as f:
            f.write(content)

        return

