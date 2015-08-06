# -*- coding:utf-8 -*-
import re

import numpy as np

from vaspy import VasPy


class OsziCar(VasPy):
    def __init__(self, filename='OSZICAR'):
        VasPy.__init__(self, filename)

        #set regex patterns
        float_regex = r'[\+|-]?\d*\.\d*(?:E[\+|-]?\d+)?'
        eq_regex = r'\s*([\w|\d|\s]+)\=\s*(' + float_regex + r')\s*'
        split_regex = r'^\s*(\d+)\s*((' + eq_regex + r')+)$'  # 将step和其余部分分开

        self.eq_regex = re.compile(eq_regex)
        self.split_regex = re.compile(split_regex)

        self.load()

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.__repr__()

    def match(self, line):
        m = self.split_regex.search(line)
        if m:
            #get step
            step = int(m.group(1))
            #get other data
            resid = m.group(2)
            eq_tuples = self.eq_regex.findall(resid)  # list of tuples
            names, numbers = zip(*eq_tuples)
            #remove space in names
            names = [name.replace(' ', '') for name in names]
            #convert string to float
            numbers = [float(number) for number in numbers]
            eq_tuples = [('step', step)] + zip(names, numbers)
            return eq_tuples
        else:
            return None

    def load(self):
        with open(self.filename, 'r') as f:
            content = ''
            for line in f:
                eq_tuples = self.match(line)
                if eq_tuples:  # if matched
                    if not hasattr(self, 'vars'):
                        self.vars, numbers = zip(*eq_tuples)
                    for name, number in eq_tuples:
                        if not hasattr(self, name):
                            setattr(self, name, [number])
                        else:
                            getattr(self, name).append(number)
                    content += line
            self.content = content
            #convert list to numpy array
            for var in self.vars:
                data = getattr(self, var)
                setattr(self, var, np.array(data))

        return

    def esort(self, n, reverse=False):
        '''
        进行能量排序, 获取排序后的前n个值.
        '''
        zipped = zip(self.E0, self.step)  # (E0, step)
        dtype = [('E0', float), ('step', int)]
        zipped = np.array(zipped, dtype=dtype)
        srted = np.sort(zipped, order='E0')

        if reverse:
            return srted[-n:]
        else:
            return srted[:n]
