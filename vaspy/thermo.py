# -*- coding:utf-8 -*-
import re

import numpy as np

from vaspy import VasPy


class OsziCar(VasPy):
    def __init__(self, filename='OSZICAR'):
        VasPy.__init__(self, filename)

        #set regex patterns
        float_regex = r'[\+|-]?\d*\.\d+(?:E[\+|-]?\d+)?'
        step = r'\s*(\d+)\s*'
        F = r'F\=\s*(' + float_regex + r')\s*'
        E0 = r'E0\=\s*(' + float_regex + r')\s*'
        dE = r'd\s*E\s*\=(' + float_regex + r')\s*'
        mag = r'mag\=\s*(' + float_regex + r')\s*'
        self.regex = re.compile(step + F + E0 + dE + mag)

        self.load()

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.__repr__()

    def match(self, line):
        m = self.regex.search(line)
        if m:
            step, F, E0, dE, mag = m.groups()
            #type convertion
            step = int(step)
            F, E0, dE, mag = [float(i) for i in m.groups()[1:]]
            return step, F, E0, dE, mag
        else:
            return None

    def load(self):
        with open(self.filename, 'r') as f:
            steps, Fs, E0s, dEs, mags = [], [], [], [], []
            content = ''
            for line in f:
                data = self.match(line)
                if data:  # if matched
                    step, F, E0, dE, mag = data
                    steps.append(step)
                    Fs.append(F)
                    E0s.append(E0)
                    dEs.append(dE)
                    mags.append(mag)
                    content += line
        #set class attrs
        self.step = np.array(steps)
        self.F = np.array(Fs)
        self.E0 = np.array(E0s)
        self.dE = np.array(dEs)
        self.mag = np.array(mags)
        self.content = content

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
