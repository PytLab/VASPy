'''
    Script to create .xyz file.
'''
import argparse
import commands
import logging
import re
import sys

from vaspy import atomco, matstudio
from vaspy.iter import OutCar, OsziCar

if "__main__" == __name__:

    # Set argument parser.
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--step",
                        help="step number on which the data is extracted.")
    args = parser.parse_args()

    if args.step:
        # extract certain step data to .xyz file
        step = args.step
        step_regex = re.compile(r'^STEP\s+=\s+' + step + r'$')
        with open('OUT.ANI', 'r') as f:
            natom = int(f.readline().strip())
            # match step
            content = ''
            count = 0
            line = f.readline()
            while line:
                if step_regex.match(line):
                    # get data content
                    for i in xrange(natom):
                        content += f.readline()
                    break
                line = f.readline()
            if not content:
                print 'Step: %s is out of range.' % step
                sys.exit(1)
        # write to .xyz file
        with open('ts.xyz', 'w') as f:
            head = '%12d\nSTEP = %8s\n' % (natom, step)
            content = head + content
            f.write(content)

        # coordinate transformation
        xyz = atomco.XyzFile('ts.xyz')
        poscar = atomco.PosCar()
        direct_coordinates = xyz.coordinate_transform(poscar.bases)
        suffix = '-' + step + '.xsd'
    else:  # the last step data
        contcar = atomco.ContCar()
        direct_coordinates = contcar.data
        suffix = '-y.xsd'

# create .xsd file
status, output = commands.getstatusoutput('ls *.xsd | head -1')
if not output.endswith('.xsd'):
    print "No .xsd file in current directory."
    sys.exit(1)
xsd = matstudio.XsdFile(filename=output)
xsd.data = direct_coordinates

# Get energy and force.
oszicar = OsziCar()
outcar = OutCar()
xsd.force = outcar.total_forces[-1]
logging.info("Total Force --> {}".format(xsd.force))
xsd.energy = oszicar.E0[-1]
logging.info("Total Energy --> {}".format(xsd.energy))

jobname = output.split('.')[0]
xsd.tofile(filename=jobname+suffix)
