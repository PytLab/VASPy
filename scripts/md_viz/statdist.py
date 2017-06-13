#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy.linalg import norm

from vaspy.iter import XdatCar, AniFile

fixed_coord = [0.00000000, 1.92610195, 10.69285799]
O_index = 1
max_x = 0.5
max_y = 0.5

def pdc_coord(coord):
    ''' Process the coordinate using PDC.
    '''
    new_coord = [0.0]*3
    for i, c in enumerate(coord):
        if (i == 0 and c > max_x) or (i == 1 and c > max_y):
            c -= 1.0
        new_coord[i] = c

    return new_coord

if '__main__' == __name__:
    ani = AniFile()
    xdatcar = XdatCar()

    fixed_coord = xdatcar.dir2cart(xdatcar.bases, pdc_coord(xdatcar.cart2dir(xdatcar.bases, fixed_coord)))

    atoms = [0]*5

    for xyz in ani:
        coord = xyz.data[O_index]
        # Convert cartesian to direct.
        dir_coord = xdatcar.cart2dir(xdatcar.bases, coord)
        dir_coord = pdc_coord(dir_coord)

        # Convert coordinate back to cartesian coordinate.
        cart_coord = xdatcar.dir2cart(xdatcar.bases, dir_coord)

        # Distance.
        distance = norm(cart_coord - np.array(fixed_coord))

        if 0.0 < distance < 0.2:
            atoms[0] += 1
        elif 0.2 < distance < 0.4:
            atoms[1] += 1
        elif 0.4 < distance < 0.6:
            atoms[2] += 1
        elif 0.6 < distance < 0.8:
            atoms[3] += 1
        elif 0.8 < distance < 1.0:
            atoms[4] += 1
        else:
            print('WARNING: {} -> {}, distance: {}'.format(cart_coord, fixed_coord, distance))

    with open('result.txt', 'w') as f:
        f.write('atoms = {}'.format(atoms))
