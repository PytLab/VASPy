'''
    Script to convert .xsd file to VASP input files.
'''

import argparse
import commands
import os
import sys
import logging

import numpy as np

from vaspy.matstudio import XsdFile
from vaspy.incar import InCar

if "__main__" == __name__:

    # Set argument parser.
    parser = argparse.ArgumentParser()

    # Add kpoint optional argument.
    parser.add_argument("-k", "--kpoints", help="set k-points")
    args = parser.parse_args()

    # create POSCAR
    status, output = commands.getstatusoutput('ls *.xsd | head -1')
    xsd = XsdFile(filename=output)
    poscar_content = xsd.get_poscar_content(bases_const=1.0)
    with open('POSCAR', 'w') as f:
        f.write(poscar_content)

    # create POTCAR
    potdir = r'/data/pot/vasp/potpaw_PBE2010/'
    # delete old POTCAR
    if os.path.exists('./POTCAR'):
        os.remove('./POTCAR')
    for elem in xsd.atoms:
    #    if os.path.exists(potdir + elem + '_new/'):
    #        potcar = potdir + elem + '_new/POTCAR'
        if os.path.exists(potdir + elem):
            potcar = potdir + elem + '/POTCAR'
        else:
            print 'No POTCAR for ' + elem
            sys.exit(1)
        commands.getstatusoutput('cat ' + potcar + ' >> ./POTCAR')

    # creat KPOINTS
    if not args.kpoints:
        kpoints = []
        for base in xsd.bases:
            l = np.dot(base, base)**0.5
            kpt = int(20/l) + 1
            kpoints.append(str(kpt))
    else:
        kpoints = [i.strip() for i in args.kpoints.split(",")]
        logging.info("Set k-point -> {} {} {}".format(*kpoints))
    kpt_str = ' '.join(kpoints)
    kpt_content = 'mesh auto\n0\nG\n' + kpt_str + '\n0 0 0\n'
    with open('KPOINTS', 'w') as f:
        f.write(kpt_content)

    # copy INCAR vasp.script
    commands.getstatusoutput('cp $HOME/example/INCAR $HOME/example/vasp.script ./')
    # change jobname
    jobname = output.split('.')[0]
    with open('vasp.script', 'r') as f:
        content_list = f.readlines()

    content_list[1] = '#PBS -N ' + jobname + '\n'
    with open('vasp.script', 'w') as f:
        f.writelines(content_list)

    # create fort.188
    atom_idxs = []
    atom_names = []
    for idx, atom_name in enumerate(xsd.atom_names):
        if atom_name.endswith('_c'):
            atom_idxs.append(idx)
            atom_names.append(atom_name)
    # if constrained get distance and create fort.188
    if atom_idxs:
        if len(atom_idxs) > 2:
            raise ValueError("More than two atoms end with '_c'")
        pt1, pt2 = [xsd.data[idx, :] for idx in atom_idxs]
        # use Ax=b convert to cartisan coordinate
        diff = pt1 - pt2
        A = np.matrix(xsd.bases.T)
        x = np.matrix(diff).T
        b = A*x
        distance = np.linalg.norm(b)
        # create fort.188
        content = '1\n3\n6\n4\n0.04\n%-5d%-5d%f\n0\n' % \
            (atom_idxs[0]+1, atom_idxs[1]+1, distance)
        with open('fort.188', 'w') as f:
            f.write(content)
        logging.info("fort.188 has been created.")
        logging.info('-'*20)
        logging.info("atom number: {:<5d}{:<5d}".format(atom_idxs[0]+1, atom_idxs[1]+1))
        logging.info("atom name: {} {}".format(*atom_names))
        logging.info("distance: {:f}".format(distance))
        logging.info('-'*20)

        # set IBRION = 1
        incar = InCar()
        incar.set('IBRION', 1)
        incar.tofile()
        logging.info("IBRION is set to 1.")
