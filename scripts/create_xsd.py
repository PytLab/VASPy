#!/usr/bin/env python
'''
Script to create xsd file from VASP outputs.
'''

import argparse
import logging
import re
import sys

from vaspy import atomco, matstudio
from vaspy.iter import OutCar, OsziCar
from vaspy import PY2

if PY2:
    import commands as subprocess
else:
    import subprocess

_logger = logging.getLogger("vaspy.script")


if "__main__" == __name__:

    # Set argument parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--step",
                        help="step number on which the data is extracted.")
    args = parser.parse_args()

    if args.step:
        # extract certain step data to .xyz file
        step = int(args.step)

        # Get data of that step from XDATCAR.
        xdatcar = atomco.XdatCar()
        for i, data in xdatcar:
            if i == step:
                break

        # Check step validity.
        if i < step:
            raise ValueError("Illegal step {} (> {})".format(step, i))

        # Direct coordinates for that step.
        direct_coordinates = data

        suffix = "-{}.xsd".format(step)
    else:  # the last step data
        contcar = atomco.ContCar()
        direct_coordinates = contcar.data
        suffix = '-y.xsd'

    # create .xsd file
    status, output = subprocess.getstatusoutput('ls *.xsd | head -1')
    if not output.endswith('.xsd'):
        _logger.info("No .xsd file in current directory.")
        sys.exit(1)
    xsd = matstudio.XsdFile(filename=output)
    xsd.data = direct_coordinates

    # Get energy and force.
    oszicar = OsziCar()
    outcar = OutCar()

    # Get force and energy for specific step.
    idx = int(args.step)-1 if args.step else -1
    xsd.force = outcar.total_forces[idx]
    _logger.info("Total Force --> {}".format(xsd.force))
    xsd.energy = oszicar.E0[idx]
    _logger.info("Total Energy --> {}".format(xsd.energy))

    jobname = output.split('.')[0]
    xsd.tofile(filename=jobname+suffix)
    _logger.info("{} created.".format(jobname+suffix))

