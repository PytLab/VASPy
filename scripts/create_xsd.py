'''
    Script to convert CONTCAR to .xsd file
'''
import commands
import sys
from vaspy.matstudio import XsdFile
from vaspy.atomco import PosCar

status, output = commands.getstatusoutput('ls *.xsd | head -1')
if not output.endswith('.xsd'):
    print "No .xsd file in current directory."
    sys.exit(1)
xsd = XsdFile(filename=output)
poscar = PosCar(filename='CONTCAR')
xsd.data = poscar.data

jobname = output.split('.')[0]
xsd.tofile(filename=jobname+'-y.xsd')
