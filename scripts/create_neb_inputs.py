#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Script to create neb input files from Material Studio trajectory file.
"""

import argparse
import glob
import logging
import os
import re
import shutil
import sys

import numpy as np

from vaspy import PY2
from vaspy.matstudio import XtdFile, ArcFile
from vaspy.incar import InCar

if PY2:
    import commands as subprocess
else:
    import subprocess

_logger = logging.getLogger("vaspy.script")


def _exec_command(command):
    """
    Protected helper function to exec shell command and check.
    """
    status, output = subprocess.getstatusoutput(command)
    if status:
        _logger.error(output)
        sys.exit(1)

    return output



if "__main__" == __name__:
    # Set argument parser.
    parser = argparse.ArgumentParser()

    # Add optional arguments.
    parser.add_argument("-k", "--kpoints", help="set k-points")
    parser.add_argument("--nnode", help="node number used for the job")
    parser.add_argument("--ncpu", help="cpu number on each node")
    parser.add_argument("-q", "--queue", help="pbs queue type")

    # Add all possible arguments in INCAR file.
    if os.path.exists("INCAR"):
        incar = InCar()
        parameters = incar.pnames
        for parameter in parameters:
            help_info = "Set '{}' in INCAR".format(parameter)
            parser.add_argument("--{}".format(parameter), help=help_info)

    args = parser.parse_args()

    # Create XtdFile & ArcFile objects.
    arcname = _exec_command("ls *.arc | head -1")
    xtdname = _exec_command("ls *.xtd | head -1")
    xtd = XtdFile(filename=xtdname, arcname=arcname)

    # Create images.
    for idx, dir_coords in enumerate(xtd.coords_iterator):
        # Create images dir.
        dirname = str(idx).zfill(2)
        _exec_command("mkdir {}".format(dirname))
        _logger.info("{} created.".format(dirname))

        # Create image poscar.
        poscar_content = xtd.get_poscar_content(data=dir_coords)
        poscar_name = "{}/POSCAR".format(dirname)
        with open(poscar_name, "w") as f:
            f.write(poscar_content)
        _logger.info("{} created.".format(poscar_name))

    # Move OUTCAR to 00 & XX.
    if glob.glob("OUTCAR_*"):
        shutil.move("OUTCAR_00", "./00/OUTCAR")
        shutil.move("OUTCAR_XX", "./{}/OUTCAR".format(dirname))

    # Number of images.
    n_images = idx - 1

    # Copy INCAR vasp.script.
    _exec_command("cp $HOME/example/INCAR $HOME/example/vasp.script ./")

    # Create POTCAR
    potdir = r"/data/pot/vasp/potpaw_PBE2010/"
    # delete old POTCAR
    if os.path.exists("./POTCAR"):
        os.remove("./POTCAR")
    for elem in xtd.atoms:
        if os.path.exists(potdir + elem):
            potcar = potdir + elem + "/POTCAR"
        else:
            _logger.info("No POTCAR for " + elem)
            sys.exit(1)
        _exec_command("cat {} >> ./POTCAR".format(potcar))

    # Creat KPOINTS
    if not args.kpoints:
        kpoints = []
        for base in xtd.bases:
            l = np.dot(base, base)**0.5
            kpt = int(20/l) + 1
            kpoints.append(str(kpt))
    else:
        kpoints = [i.strip() for i in args.kpoints.split(",")]
        _logger.info("Set k-point -> {} {} {}".format(*kpoints))
    kpt_str = " ".join(kpoints)
    kpt_content = "mesh auto\n0\nG\n" + kpt_str + "\n0 0 0\n"
    with open("KPOINTS", "w") as f:
        f.write(kpt_content)

    # Modify INCAR parameters.
    incar = InCar()
    incar.set("IBRION", 3)
    incar.set("POTIM", 0)
    neb_parameters = [("IOPT", 1),
                      ("ICHAIN", 0),
                      ("LCLIMB", ".TRUE."),
                      ("SPRING", -5),
                      ("IMAGES", n_images)]
    for pname, value in neb_parameters:
        incar.add(pname, value)
        _logger.info("{} -> {}".format(pname, value))
    incar.tofile()

    # Modify qsub script.
    jobname = xtdname.split('.')[0]
    with open('vasp.script', 'r') as f:
        content_list = f.readlines()

    # Change job name.
    content_list[1] = '#PBS -N ' + jobname + '\n'
    _logger.info("job name -> {}".format(jobname))

    # Change node number and cpu number.
    if args.nnode or args.ncpu:
        regex = re.compile(r'nodes=(\d):ppn=(\d)')
        match = regex.search(content_list[5])
        if not match:
            msg = "Regular expressioon match error, please check your pbs script."
            raise ValueError(msg)
        nnode, ncpu = match.groups()
        nnode = args.nnode if args.nnode else nnode
        ncpu = args.ncpu if args.ncpu else ncpu
        content_list[5] = "#PBS -l nodes={}:ppn={}\n".format(nnode, ncpu)
        _logger.info("nodes -> {}, ppn -> {}".format(nnode, ncpu))

    # Change node type.
    if args.queue:
        content_list[6] = "#PBS -q {}\n".format(args.queue)
        _logger.info("queue type -> {}".format(args.queue))

    with open('vasp.script', 'w') as f:
        f.writelines(content_list)

