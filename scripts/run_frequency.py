#!/usr/bin/env python

import logging
import os

from vaspy import PY2
from vaspy.incar import InCar

if PY2:
    import commands as subprocess
else:
    import subprocess

_logger = logging.getLogger("vaspy.script")

if "__main__" == __name__:
    incar = InCar()

    # Move files.
    cmd = "cp ../KPOINTS ./"
    status, output = subprocess.getstatusoutput(cmd)
    if status:
        raise ValueError(output)
    _logger.info(cmd)

    # Change INCAR parameters.
    parameters = [("IBRION", 5), ("POTIM", 0.05), ("ISIF", 0), ("NFREE", 2)]

    for pname, value in parameters:
        if hasattr(incar, pname):
            incar.set(pname, value)
        else:
            incar.add(pname, value)
        _logger.info("{} --> {}".format(pname, value))

    incar.pop("NCORE")
    _logger.info("Remove Paramter NCORE")

    incar.tofile()

