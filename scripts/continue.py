# -*- coding:utf-8 -*-
'''
    在新的目录先自动生成相应步数的POSCAR, fort.188文件
    以及其他vasp输入文件方便继续投作业的脚本。
'''

import sys
import os

import numpy as np

from vaspy.atomco import XyzFile, PosCar
from vaspy.functions import str2list


class ContinueError(Exception):
    pass

if len(sys.argv) != 2:
    print 'Usage: %s *.xyz' % sys.argv[0]
    exit(1)
filename = sys.argv[1]

a = XyzFile(filename=filename)
b = PosCar(filename='POSCAR')
#create new dir
if not os.path.exists('./continue'):
    os.mkdir('./continue')
if os.path.isfile('./fort.188'):
    fail = os.system("cp INCAR POTCAR KPOINTS fort.188 vasp.script ./continue")
else:
    fail = os.system("cp INCAR POTCAR KPOINTS vasp.script ./continue")

if not fail:
    #new fort.188
    #change distance of 2 atoms
    with open('./continue/fort.188', 'r') as f:
        content_list = f.readlines()
    m, n, distance = str2list(content_list[5])  # atom number and distance
    x = a.data[int(m)-1, :]  # atom coordinates
    y = a.data[int(n)-1, :]
    z = x - y
    #get new distance
    new_distance = np.dot(z, z)**0.5
    newline = "%-5s%-5s%-10.6f\n" % (m, n, new_distance)
    content_list[5] = newline
    content_str = ''.join(content_list)
    #write new fort.188
    with open('./continue/fort.188', 'w') as f:
        f.write(content_str)
else:
    raise ContinueError('Failed to create continue dir.')

#add new POSCAR
data_trans = a.coordinate_transform(bases=b.bases)
b.data = data_trans
b.tofile('./continue/POSCAR')
