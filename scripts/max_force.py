import argparse
import commands
import logging
import os
import sys

import numpy as np

from vaspy.iter import OutCar
from vaspy.matstudio import XsdFile
from vaspy.functions import str2list

# Set arguments parser.
parser = argparse.ArgumentParser()
parser.add_argument("--xsd", help="create MaterStudio .xsd file",
                    action="store_true")
args = parser.parse_args()

outcar = OutCar()
max_num = outcar.max_force_atom
force_info = outcar.atom_forces[max_num-1, :]
pos = force_info[: 3].tolist()
forces = force_info[3:].tolist()

logging.info("{:<15s}: {}".format("max force atom", max_num))
logging.info("{:<15s}: ({}, {}, {})".format("atom position", *pos))
logging.info("{:<15s}: {}, {}, {}".format("forces", *forces))
logging.info("{:<15s}: {}\n".format("total-force", np.linalg.norm(forces)))

# Get fort.188 info.
if os.path.exists('./fort.188'):
    with open('fort.188', 'r') as f:
        atom_info = f.readlines()[5]
    logging.info("{:<10s}{:<10s}{:<15s}".format("Atom1", "Atom2", "DISTANCE"))
    logging.info("-"*30)
    logging.info("{:<10s}{:<10s}{:<15s}\n".format(*str2list(atom_info)))

# Create .xsd file.
if args.xsd:
    status, output = commands.getstatusoutput('ls *.xsd | head -1')
    if not output.endswith('.xsd'):
        logging.info("No .xsd file in current directory.")
        sys.exit(1)
    xsd = XsdFile(filename=output)
    # modify atom color
    xsd.modify_color(atom_number=max_num)
    jobname = output.split('.')[0]
    filename = jobname + '-force.xsd'
    xsd.tofile(filename=filename)
    print filename + " has been created."

