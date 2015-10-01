import sys
import os
import commands

import numpy as np

from vaspy.iter import OutCar
from vaspy.matstudio import XsdFile
from vaspy.functions import str2list

outcar = OutCar()
max_num = outcar.max_force_atom
force_info = outcar.atom_forces[max_num-1, :]
pos = force_info[: 3].tolist()
forces = force_info[3:].tolist()
print "\nmax force atom: %d" % max_num
print " atom position: (%f, %f, %f)" % tuple(pos)
print "        forces: %f, %f, %f" % tuple(forces)
print "   total-force: %f\n" % np.linalg.norm(forces)

# get fort.188 info
if os.path.exists('./fort.188'):
    with open('fort.188', 'r') as f:
        atom_info = f.readlines()[5]
    print "%10s%10s%15s" % ('Atom1', 'Atom2', 'DISTANCE')
    print "-"*35
    print "%10s%10s%15s\n" % tuple(str2list(atom_info))

# create .xsd file
if '--xsd' in sys.argv:
    status, output = commands.getstatusoutput('ls *.xsd | head -1')
    if not output.endswith('.xsd'):
        print "No .xsd file in current directory."
        sys.exit(1)
    xsd = XsdFile(filename=output)
    # modify atom color
    xsd.modify_color(atom_number=max_num)
    jobname = output.split('.')[0]
    filename = jobname + '-force.xsd'
    xsd.tofile(filename=filename)
    print filename + " has been created."
