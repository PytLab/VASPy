# -*- coding:utf-8 -*-
"""
========================================================================
Provide INCAR file class which do operations on these files.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, October 2015
Updated by PytLab <shaozhengjiang@gmail.com>, July 2016
Revised by jyxu <jxu15@qub.ac.uk>, October 2019
========================================================================

"""
import os 
import sys

import logging
import warnings

from vaspy import VasPy
from vaspy.vasp_para_db import *


class Param(VasPy):
    def __init__(self, pname, pvalue='', pcomm=''):
        """
        Create a INCAR parameter class.

        Example:
        >>> para = Param('SYSTEM')

        Class attributes descriptions
        =======================================================
          Attribute      Description
          ============  =======================================
          pname       string, parameter name
          pvalue      string/int/flaot, parameter value
          pcomm       string, parameter comment
          ============  =======================================

        """
        __slots__ = ('para', 'pname', 'pvalue', 'pcomm')

        self._pname, self._pvalue, self._pcomm = None, None, None

        self.pname = pname
        self.pvalue, self.pcomm = str(pvalue), str(pcomm)

        self.__logger = logging.getLogger("vaspy.Param")


    @property
    def pname(self):
        """Parameter Name"""
        return self._pname

    @pname.setter
    def pname(self, name):
        """"""
        name = name.upper()
        if name not in INCAR_PARAMETERS.keys():
            raise ValueError("Unknown Parameter <%s> in VASP INCAR Database." %name)
        self._pname = name

        return

    @property
    def pvalue(self):
        """Parameter Value"""
        return self._pvalue

    @pvalue.setter
    def pvalue(self, value):
        """"""
        optional_values = [str(v) for v in INCAR_PARAMETERS[self.pname][1]]

        # check optional values, under development
        ''' 
        if optional_values == [] or value in optional_values:
            pass
        else:
            raise ValueError("Unknown Value <%s> for Parameter <%s>." \
                    %(value, self.pname))
        '''
        
        if value != '':
            default_value = value
        else:
            default_value = INCAR_PARAMETERS[self.pname][0]

        self._pvalue = str(default_value)

        return 

    @property
    def pcomm(self):
        """Parameter Comment"""
        return self._pcomm

    @pcomm.setter
    def pcomm(self, comm):
        """"""
        if comm == '':
            comm = " ".join((COMMSIGN, INCAR_PARAMETERS[self.pname][2]))
        else:
            if not comm.startswith(COMMSIGN):
                comm = " ".join((COMMSIGN, comm))

        self._pcomm = comm

        return
    
    @property
    def para(self):
        """"""
        return (self.pname, self.pvalue, self.pcomm)
    
    def __add__(self, another):
        """
        Overload the add operator, a *Param* adds a *Param*/*Params* equal *Params*.
        """
        if isinstance(another, Param):
            return Params((self, another))
        elif isinstance(another, Params):
            return Params((self,) + another.paras)
        else:
            raise ValueError("Add must also be a *Param*/*Params* object.")

    def __repr__(self):
        return str(self.para)


class Params(VasPy):
    def __init__(self, paras=()):
        """
        Create a INCAR parameters class.
        """
        # set logger
        self.__logger = logging.getLogger("vaspy.Params")

        if paras == ():
            self.paras = ()
        elif isinstance(paras, list) or isinstance(paras, tuple):
            self.paras = self.remove_duplicates(paras)
        else:
            self("%s must be a *list* or *tuple* object." %paras)

    def remove_duplicates(self, paras):
        """Remove duplicates in paras, return a tuple"""
        paras_list = []
        for para in paras:
            if isinstance(para, Param):
                pnames = [p.pname for p in paras_list]
                if para.pname in pnames:
                    warnings.warn("Duplicate parameter " + \
                            "%s, value %s(old) %s(new), the new one is not read."\
                            %(para.pname, paras_list[pnames.index(para.pname)], \
                            para.pvalue), RuntimeWarning)
                else:
                    paras_list.append(para)
            else:
                raise ValueError("%s must be a *Param* object." %para)

        return tuple(paras_list)
    
    @property
    def pnames(self):
        """Return all parameters' names."""
        self._pnames = [p.pname for p in self.paras]

        return tuple(self._pnames)

    @property
    def pvalues(self):
        """"""
        self._pvalues = [p.pvalue for p in self.paras]

        return tuple(self._pvalues)

    def get_para(self, name):
        """"""
        return self.paras[self.pnames.index(name)]

    def get_pvalue(self, name):
        """"""
        return self.pvalues[self.pnames.index(name)]

    def __compare(self, another):
        """
        Private method to compare two Params object.
        """
        self_pnames, another_pnames = self.pnames, another.pnames
        tot_pnames = set(list(self_pnames) + list(another_pnames))

        self_dict, another_dict = {}, {}
        for pname in tot_pnames:
            # If both have, check the difference.
            if (pname in self_pnames and pname in another_pnames):
                self_pvalue = self.get_pvalue(pname)
                another_pvalue = self.get_pvalue(pname)
                if self_pvalue != another_pvalue:
                    self_dict.setdefault(pname, self_pvalue)
                    another_dict.setdefault(pname, another_pvalue)
            else:
                # Only in this object.
                if pname in self_pnames:
                    self_pvalue = self.get_pvalue(pname)
                    self_dict.setdefault(pname, self_pvalue)
                    another_dict.setdefault(pname, "")
                # Only in the other object.
                else:
                    another_pvalue = self.get_pvalue(pname)
                    another_dict.setdefault(pname, another_pvalue)
                    self_dict.setdefault(pname, "")

        return self_dict, another_dict

    def __eq__(self, another):
        """
        Overload euqal operator function.
        """
        self_dict, another_dict = self.__compare(another)
        # print(self_dict, another_dict)

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

    def __add__(self, another):
        """
        Overload add operator, append a *Param*/*Params* to a *Params*
        """
        if isinstance(another, Param):
            paras = self.paras + (another,)
        elif isinstance(another, Params):
            paras = self.paras + another.paras

        paras = self.remove_duplicates(paras)

        return Params(paras)

    def add(self, pname, pvalue=''):
        """
        Add a new parameter to *Params* object.
        Now only param object are supported.
        Different from __add__, which does not change the *Param* object.

        Example:
        --------
        >>> paras.add('ISIF', 2)
        """
        para = Param(pname, pvalue)
        paras = (self + para).paras
        self.paras = paras

        return self

    def __sub__(self, another):
        """
        Overload sub operator, remove a *Param*/*Params* to a *Params*
        """
        if isinstance(another, Param):
            paras = (para for para in self.paras if para.pname != another.pname)
        elif isinstance(another, Params):
            paras = (para for para in self.paras if para.pname not in another.pnames)

        self.paras = tuple(paras)

        return self

    def set(self, name, value):
        """
        Set a named parameter of InCar object.

        Example:
        --------
        >>> incar_obj.set("ISIF", 2)
        """
        if name not in self.pnames:
            raise ValueError('%s is not in INCAR, ' + 'Use add() instead.' % name)
        
        self.get_para(name).pvalue = str(value)

        return
    
    def pop(self, pname):
        """
        Delete a parameter from InCar object.

        Returns:
        --------
        parameter name, parameter value.

        Example:
        --------
        >>> incar_obj.pop("ISIF")
        """
        if pname not in self.pnames:
            raise ValueError('%s is not in INCAR, ' + 'Use add() instead.' % name)

        # Delete from pnames and datas.
        value = self.get_pvalue(pname)
        paras = (self - self.get_para(pname)).paras 
        self.paras = paras

        return pname, value

    def __len__(self):
        """
        Overload len operator, return the number of parameters.
        """
        return len(self.paras)

    def __repr__(self):
        """
        """
        return str(self.paras)


class InCar(Params):
    def __init__(self, src='INCAR'):
        """
        Create a INCAR file class.

        Example:

        >>> a = InCar()

        Class attributes descriptions
        =======================================================
          Attribute      Description
          ============  =======================================
          src           string/Params, incar parameter source
          ============  =======================================
        """
        # super(self.__class__, self).__init__(src)
        if src == 'INCAR':
            if not os.path.exists('INCAR'):
                src = None

        if src is None:
            self.paras = ()
        else:
            if isinstance(src, str):
                if os.path.isfile(src):
                    self.filename = src
                    self.paras = self.load()
            elif isinstance(src, Params):
                self.paras = src.paras

        if self.paras != ():
            self.paras = self.remove_duplicates(self.paras)
        self.parasets = None

        # set logger
        self.__logger = logging.getLogger("vaspy.InCar")

    def load(self):
        "Load all data in INCAR."
        tot_pnames, tot_pvalues, tot_pcomms = [], [], []
        with open(self.filename, 'r') as reader:
            for line in reader:
                matched = self.rdata(line)
                if matched:
                    pnames, pvalues, pcomms = matched
                    tot_pnames.extend(pnames)
                    tot_pvalues.extend(pvalues)
                    tot_pcomms.extend(pcomms)

        paras_list = []
        for pname, pvalue, pcomm in zip(tot_pnames, tot_pvalues, tot_pcomms):
            para = Param(pname, pvalue, pcomm)
            paras_list.append(para)

        return tuple(paras_list)

    @staticmethod
    def rdata(line):
        "Get INCAR data(s) in a line."
        line = line.strip()
        if not line or line.startswith(('!', '#')):
            return None
        else:
            pnames, pvalues, pcomms = [], [], []
            value, comm = '', ''
            if '#' in line:
                splitted_line = line.split('#')
                value = splitted_line[0].strip()
                comm = splitted_line[1].strip()
                if '!' in value:
                    splitted_value = value.split('!')
                    value = splitted_value[0].strip()
                    comm = ' '.join(comm, splitted_value[1].strip())
            elif '!' in line:
                splitted_line = line.split('!')
                value = splitted_line[0].strip()
                comm = splitted_line[1].strip()
                if '#' in value:
                    splitted_value = value.split('#')
                    value = splitted_value[0].strip()
                    comm = ' '.join(comm, splitted_value[1].strip())
            else:
                value = line
            pcomms.append(comm)
            # get parameter name and data
            if ';' in value:
                params = [param.strip() for param in value.split(';')]
            else:
                params = [value]
            for param in params:
                pname, pvalue = [i.strip() for i in param.split('=')]
                pnames.append(pname)
                pvalues.append(pvalue)

            return pnames, pvalues, pcomms

    def quickgen(self, tasks, **kargs):
        """Quick generation of INCAR with built-in parameters."""
        # check task
        tasks = tasks.strip().split('-')

        # check if SC in tasks
        task_basic = ['SC']
        if 'SC' not in tasks:
            task_basic.extend(tasks)
            tasks = task_basic

        parasets = []
        for task in tasks:
            if task in BUILTIN_PARASETS.keys():
                parasets.extend(BUILTIN_PARASETS[task][0])
            else:
                msg = "Unsupported INCAR parameter set %s." %task
                self.__logger.error(msg)
                sys.exit(1)

        self.parasets = parasets

        # load parasets
        self.incar_categories = INCAR_PARACATEGORIES
        pnames = []
        for pset in self.parasets:
            pnames.extend(list(self.incar_categories[pset]))

        paras_list = []
        for pname in pnames:
            paras_list.append(Param(pname))

        self.paras = tuple(paras_list)

        # special settings for some task
        paras_list = []
        for task in tasks:
            for para in BUILTIN_PARASETS[task][1]:
                self.get_para(para[0]).pvalue = para[1]

        # add more parameters along with built-in parasets
        for key, value in kargs.items():
            self.set(key, str(value))

        return 

    def tostr(self):
        """"""
        content = '# Created by VASPy\n'
        if self.parasets:
            tot_pnames = []
            for pset in self.parasets:
                content += '# %s\n' %pset
                pnames = INCAR_PARACATEGORIES[pset]
                tot_pnames.extend(pnames)
                for pname in pnames:
                    para = self.get_para(pname)
                    content += PARAFORMAT.format(para.pname, para.pvalue, para.pcomm)
                content += '\n' 

            other_pnames = [pname for pname in self.pnames \
                    if pname not in tot_pnames]
            if len(other_pnames) != 0:
                content += '# Additional\n'
                for pname in other_pnames:
                    para = self.get_para(pname)
                    content += PARAFORMAT.format(para.pname, para.pvalue, para.pcomm)
                content += '\n' 
        else:
            for para in self.paras:
                content += PARAFORMAT.format(para.pname, para.pvalue, para.pcomm)

        return content
    
    def tofile(self, filename='INCAR', verbos=True):
        "Create INCAR file."
        if filename is None:
            self.__logger.error("Filename to write INCAR is needed.")
        else:
            if os.path.exists(filename):
                self.__logger.warning("%s exists will be overrided." %filename)

        content = self.tostr()
        with open(filename, 'w') as writer:
            writer.write(content)

        self.__logger.info("Succesfully write incar obejct to %s." %filename)

        if verbos:
            print(content)

        return
    
    def __repr__(self):
        """"""
        return self.tostr()

