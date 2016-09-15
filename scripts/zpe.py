#!/usr/bin/env python

import logging

from vaspy.iter import OutCar

_logger = logging.getLogger("vaspy.script")

if "__main__" == __name__:
    outcar = OutCar()
    poscar = outcar.poscar
    freq_types = outcar.freq_types

    # Frequency info.
    _logger.info("{:<10s}{:<10s}{:<20s}".format("atom", "type", "freq_type"))
    _logger.info("-"*35)

    # Get atom types.
    atom_types = []
    for t, n in zip(poscar.atoms, poscar.atoms_num):
        atom_types += [t]*n

    idx = 0
    tfs = poscar.tf.tolist()
    for atom_idx, tf in enumerate(tfs):
        if tf == ["T", "T", "T"]:
            msg = "{:<10d}{:<10s}{:<5s}{:<5s}{:<5s}"
            msg = msg.format(atom_idx+1, atom_types[atom_idx], *freq_types[idx])
            _logger.info(msg)
            idx += 1

    # Zero point energy.
    _logger.info("")
    _logger.info("ZPE = {}".format(outcar.zpe))

