#!/usr/bin/env python
'''
    Script to convert .xsd file to VASP input files.
'''

import argparse
import os
import re
import sys
import logging

import numpy as np

from vaspy.matstudio import XsdFile
from vaspy.incar import InCar
from vaspy import PY2

if PY2:
    import commands as subprocess
else:
    import subprocess

_logger = logging.getLogger("vaspy.script")


if "__main__" == __name__:

    # Copy INCAR vasp.script
    subprocess.getstatusoutput('cp $HOME/example/INCAR $HOME/example/vasp.script ./')

    # Set argument parser.
    parser = argparse.ArgumentParser()

    # Add optional argument.
    parser.add_argument("-k", "--kpoints", help="set k-points")
    parser.add_argument("--nnode", help="node number used for the job")
    parser.add_argument("--ncpu", help="cpu number on each node")
    parser.add_argument("-q", "--queue", help="pbs queue type")

    # Add all possible arguments in INCAR file.
    if os.path.exists("INCAR"):
        incar = InCar()
        parameters = incar.pnames
        for parameter in parameters:
            help_info = "Set '{}' in INCAR".format(parameter)
            parser.add_argument("--{}".format(parameter), help=help_info)

    args = parser.parse_args()

    # Create POSCAR
    status, output = subprocess.getstatusoutput('ls *.xsd | head -1')
    xsd = XsdFile(filename=output)
    poscar_content = xsd.get_poscar_content(bases_const=1.0)
    with open('POSCAR', 'w') as f:
        f.write(poscar_content)

    # Create POTCAR
    potdir = r'/data/pot/vasp/potpaw_PBE2010/'
    # delete old POTCAR
    if os.path.exists('./POTCAR'):
        os.remove('./POTCAR')
    for elem in xsd.atom_types:
    #    if os.path.exists(potdir + elem + '_new/'):
    #        potcar = potdir + elem + '_new/POTCAR'
        if os.path.exists(potdir + elem):
            potcar = potdir + elem + '/POTCAR'
        else:
            _logger.info('No POTCAR for ' + elem)
            sys.exit(1)
        subprocess.getstatusoutput('cat ' + potcar + ' >> ./POTCAR')

    # Creat KPOINTS
    if not args.kpoints:
        kpoints = []
        for base in xsd.bases:
            l = np.dot(base, base)**0.5
            kpt = int(20/l) + 1
            kpoints.append(str(kpt))
    else:
        kpoints = [i.strip() for i in args.kpoints.split(",")]
        _logger.info("Set k-point -> {} {} {}".format(*kpoints))
    kpt_str = ' '.join(kpoints)
    kpt_content = 'mesh auto\n0\nG\n' + kpt_str + '\n0 0 0\n'
    with open('KPOINTS', 'w') as f:
        f.write(kpt_content)

    # Get content line list.
    jobname = ".".join(output.split('.')[: -1])
    with open('vasp.script', 'r') as f:
        content_list = f.readlines()

    # Change job name.
    content_list[1] = '#PBS -N ' + jobname + '\n'
    _logger.info("job name -> {}".format(jobname))

    # Change node number and cpu number.
    if args.nnode or args.ncpu:
        regex = re.compile(r'nodes=(\d):ppn=(\d)')
        match = regex.search(content_list[5])
        if not match:
            msg = "Regular expressioon match error, please check your pbs script."
            raise ValueError(msg)
        nnode, ncpu = match.groups()
        nnode = args.nnode if args.nnode else nnode
        ncpu = args.ncpu if args.ncpu else ncpu
        content_list[5] = "#PBS -l nodes={}:ppn={}\n".format(nnode, ncpu)
        _logger.info("nodes -> {}, ppn -> {}".format(nnode, ncpu))

    # Change node type.
    if args.queue:
        content_list[6] = "#PBS -q {}\n".format(args.queue)
        _logger.info("queue type -> {}".format(args.queue))

    with open('vasp.script', 'w') as f:
        f.writelines(content_list)

    # Create fort.188
    atom_idxs = []
    atom_names = []
    for idx, atom_name in enumerate(xsd.atom_names):
        if atom_name.endswith('_c'):
            atom_idxs.append(idx)
            atom_names.append(atom_name)
    # If constrained get distance and create fort.188
    if atom_idxs:
        if len(atom_idxs) > 2:
            raise ValueError("More than two atoms end with '_c'")
        pt1, pt2 = [xsd.data[idx, :] for idx in atom_idxs]
        # Use Ax=b convert to cartisan coordinate
        diff = pt1 - pt2
        A = np.matrix(xsd.bases.T)
        x = np.matrix(diff).T
        b = A*x
        distance = np.linalg.norm(b)
        # Create fort.188
        content = '1\n3\n6\n4\n0.04\n%-5d%-5d%f\n0\n' % \
            (atom_idxs[0]+1, atom_idxs[1]+1, distance)
        with open('fort.188', 'w') as f:
            f.write(content)
        _logger.info("fort.188 has been created.")
        _logger.info('-'*20)
        _logger.info("atom number: {:<5d}{:<5d}".format(atom_idxs[0]+1, atom_idxs[1]+1))
        _logger.info("atom name: {} {}".format(*atom_names))
        _logger.info("distance: {:f}".format(distance))
        _logger.info('-'*20)

        # Set IBRION = 1
        incar.set('IBRION', 1)
        _logger.info("{} -> {}".format("IBRION", "1"))

    if PY2:
        pname_value_pairs = args.__dict__.iteritems()
    else:
        pname_value_pairs = args.__dict__.items()

    for pname, value in pname_value_pairs :
        if (value is not None) and (pname in incar.pnames):
            incar.set(pname, value)
            _logger.info("{} -> {}".format(pname, value))

    # Generate new INCAR file.
    incar.tofile()

