'''
    Script to convert .xsd file to VASP input files.
'''
import commands
import os
import sys

import numpy as np

from vaspy.matstudio import XsdFile

#create POSCAR
status, output = commands.getstatusoutput('ls *.xsd | head -1')
xsd = XsdFile(filename=output)
poscar_content = xsd.get_poscar_content(bases_const=1.0)
with open('POSCAR', 'w') as f:
    f.write(poscar_content)

#create POTCAR
potdir = r'/data/pot/vasp/potpaw_PBE2010/'
#delete old POTCAR
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
#change jobname
jobname = output.split('.')[0]
with open('vasp.script', 'r') as f:
    content_list = f.readlines()

content_list[1] = '#PBS -N ' + jobname + '\n'
with open('vasp.script', 'w') as f:
    f.writelines(content_list)

#create fort.188
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
    # convert to cartisan coordinate
    pt1 = np.dot(xsd.bases, pt1)
    pt2 = np.dot(xsd.bases, pt2)
    distance = np.linalg.norm(pt1 - pt2)
    # create fort.188
    content = '1\n3\n6\n4\n0.04\n%-5d%-5d%f\n0\n' % \
        (atom_idxs[0]+1, atom_idxs[1]+1, distance)
    with open('fort.188', 'w') as f:
        f.write(content)
    print "fort.188 has been created."
    print "atom number: %-5d%-5d" % (atom_idxs[0]+1, atom_idxs[1]+1)
    print "atom name: %s %s" % tuple(atom_names)
    print "distance: %f" % distance
