#!/usr/bin/env python

'''
    Script to convert XDATCAR to *.arc file to display in Material Studio.
'''
import numpy as np

from vaspy.atomco import XdatCar
from vaspy.functions import get_angle

xdatcar = XdatCar()

x, y, z = xdatcar.bases
# lattice info
# angles
alpha = get_angle(y, z)
beta = get_angle(x, z)
gamma = get_angle(x, y)
# length
lx = np.linalg.norm(x)
ly = np.linalg.norm(y)
lz = np.linalg.norm(z)

content = '!BIOSYM archive 3\nPBC=ON\n'

for step, data in xdatcar:
    print("step = %s" % step)
    content += ('%80.4f\n' % 0.0)
    content += '!DATE     Oct 29 11:16:38 2015\n'
    content += 'PBC%10.4f%10.4f%10.4f%10.4f%10.4f%10.4f\n' %\
               (lx, ly, lz, alpha, beta, gamma)
    # data
    data = xdatcar.dir2cart(xdatcar.bases, data)

    atom_names = []
    for n, atom in zip(xdatcar.atoms_num, xdatcar.atoms):
        atom_names.extend([atom]*n)
    for atom_name, coord in zip(atom_names, data):
        coord = coord.tolist()[0]
        content += '%2s%16.9f%16.9f%16.9f%5s%2d%8s%8s%7.3f\n' %\
                   (atom_name, coord[0], coord[1], coord[2],
                    'XXXX', 1, 'xx', atom_name, 0.0)
    content += 'end\nend\n'

with open('xdatcar.arc', 'w') as f:
    f.write(content)
