'''
    Script to create .xyz file.
'''
import sys
import re
import commands

import vaspy

if len(sys.argv) > 1:
    # extract certain step data to .xyz file
    step = sys.argv[1]
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
        if not content:
            print 'Step: %s is out of range.' % step
            sys.exit(1)
    # write to .xyz file
    with open('ts.xyz', 'w') as f:
        head = '%12d\nSTEP = %8s\n' % (natom, step)
        content = head + content
        f.write(content)

    # coordinate transformation
    xyz = vaspy.atomco.XyzFile('ts.xyz')
    poscar = vaspy.atomco.PosCar()
    direct_coordinates = xyz.coordinate_transform(poscar.bases)
    suffix = '-' + step + ' .xsd'
else:  # the last step data
    contcar = vaspy.atomco.ContCar()
    direct_coordinates = contcar.data
    suffix = '-y.xsd'

# create .xsd file
status, output = commands.getstatusoutput('ls *.xsd | head -1')
if not output.endswith('.xsd'):
    print "No .xsd file in current directory."
    sys.exit(1)
xsd = vaspy.matstudio.XsdFile(filename=output)
xsd.data = direct_coordinates

jobname = output.split('.')[0]
xsd.tofile(filename=jobname+suffix)
