import logging
import os

from vaspy import PY2
from vaspy.incar import InCar

if PY2:
    import commands as subprocess
else:
    import subprocess

if "__main__" == __name__:
    incar = InCar()

    # Move files.
    cmd = "mv ../KPOINTS ./"
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        raise ValueError(output)

    # Change INCAR parameters.
    incar.add("IBRION", 5)
    logging.info("IBRION --> {}".format(5))
    incar.add("POTIM", 0.05)
    logging.info("POTIM --> {}".format(0.05))
    incar.add("ISIF", 0)
    logging.info("ISIF --> {}".format(0))
    incar.add("NFREE", 2)
    logging.info("NFREE --> {}".format(2))
    incar.pop("NCORE")
    logging.info("Remove Paramter NCORE")

    incar.tofile()

