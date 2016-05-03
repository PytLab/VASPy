'''
Modify recursively parameters in all INCAR file.
'''

import argparse
import commands
import logging


from vaspy.incar import InCar

SHELL_COMMAND = "find ./ -name 'INCAR'"

if "__main__" == __name__:

    # Check command validity.
    status, output = commands.getstatusoutput(SHELL_COMMAND)
    if status:
        raise SystemExit("Invalid shell commands - '{}'".format(SHELL_COMMAND))

    # Get InCar objects.
    incar_paths = (incar_path.strip() for incar_path in output.split('\n'))
    incars = [InCar(incar_path) for incar_path in incar_paths]

    # Get all possible arguments.
    set_list = [set(incar.pnames()) for incar in incars]
    possible_args = set.intersection(*set_list)

    # Set arguments for this script.
    parser = argparse.ArgumentParser()
    for arg in possible_args:
        arg_str = "--{}".format(arg)
        parser.add_argument(arg_str, help="set {} INCAR parameter".format(arg))
    args_space = parser.parse_args()

    # Change parameters for all incars.
    for pname, value in args_space.__dict__.iteritems():
        if value is None:
            continue

        for incar in incars:
            logging.info("{} --> {} in {}.".format(pname, value, incar.filename()))
            incar.set(pname, value)
            incar.tofile()

    logging.info("{} INCAR files ... ok.".format(len(incars)))

