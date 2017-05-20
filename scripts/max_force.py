#!/usr/bin/env python

import argparse
import logging
import os
import sys

from vaspy import PY2
if PY2:
    import commands as subprocess
else:
    import subprocess

import numpy as np

from vaspy.iter import OutCar
from vaspy.matstudio import XsdFile
from vaspy.functions import str2list

_logger = logging.getLogger("vaspy.script")

# Set arguments parser.
parser = argparse.ArgumentParser()
parser.add_argument("--xsd", help="create MaterStudio .xsd file",
                    action="store_true")
args = parser.parse_args()

outcar = OutCar()
pos, forces = outcar.forces(-1)
idx = outcar.last_max_atom - 1
pos = pos[idx]
forces = forces[idx]

_logger.info("{:<15s}: {}".format("max force atom", outcar.last_max_atom))
_logger.info("{:<15s}: ({}, {}, {})".format("atom position", *pos))
_logger.info("{:<15s}: {}, {}, {}".format("forces", *forces))
_logger.info("{:<15s}: {}\n".format("total-force", outcar.last_max_force))

# Get fort.188 info.
if os.path.exists('./fort.188'):
    with open('fort.188', 'r') as f:
        atom_info = f.readlines()[5]
    _logger.info("{:<10s}{:<10s}{:<15s}".format("Atom1", "Atom2", "DISTANCE"))
    _logger.info("-"*30)
    _logger.info("{:<10s}{:<10s}{:<15s}\n".format(*str2list(atom_info)))

# Create .xsd file.
if args.xsd:
    status, output = subprocess.getstatusoutput('ls *.xsd | head -1')
    if not output.endswith('.xsd'):
        _logger.info("No .xsd file in current directory.")
        sys.exit(1)
    xsd = XsdFile(filename=output)
    # modify atom color
    xsd.modify_color(atom_number=outcar.last_max_atom)
    jobname = output.split('.')[0]
    filename = jobname + '-force.xsd'
    xsd.tofile(filename=filename)
    _logger.info(filename + " has been created.")

