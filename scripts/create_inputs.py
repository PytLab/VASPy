'''
    Script to convert .xsd file to VASP input files.
'''
import commands
import os
import sys

import numpy as np

from vaspy.matstudio import XsdFile

status, output = commands.getstatusoutput('ls *.xsd | head -1')
xsd = XsdFile(filename=output)
poscar_content = xsd.get_poscar_content(bases_const=1.0)
with open('POSCAR', 'w') as f:
    f.write(poscar_content)

#create POTCAR
potdir = r'/data/pot/vasp/potpaw_PBE2010/'
for elem in xsd.atoms:
    if os.path.exists(potdir + elem + '_new/'):
        potcar = potdir + elem + '_new/POTCAR'
    elif os.path.exists(potdir + elem):
        potcar = potdir + elem + '/POTCAR'
    else:
        print 'No POTCAR for ' + elem
        sys.exit(1)
    commands.getstatusoutput('cat ' + potcar + ' >> ./POTCAR')

#creat KPOINTS
kpoints = []
for base in xsd.bases:
    l = np.dot(base, base)**0.5
    kpt = int(20/l) + 1
    kpoints.append(str(kpt))
kpt_str = ' '.join(kpoints)
kpt_content = 'mesh auto\n0\nG\n' + kpt_str + '\n0 0 0\n'
with open('KPOINTS', 'w') as f:
    f.write(kpt_content)

#copy INCAR vasp.script
commands.getstatusoutput('cp $HOME/example/INCAR $HOME/example/vasp.script ./')
