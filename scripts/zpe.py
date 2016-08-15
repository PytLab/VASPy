import logging

from vaspy.iter import OutCar

_logger = logging.getLogger("vaspy.script")

if "__main__" == __name__:
    outcar = OutCar()
    poscar = outcar.poscar
    freq_types = outcar.freq_types

    # Frequency info.
    _logger.info("{:<10s}{:<20s}".format("atom", "freq_type"))
    _logger.info("-"*25)

    idx = 0
    tfs = poscar.tf.tolist()
    for atom_idx, tf in enumerate(tfs):
        if tf == ["T", "T", "T"]:
            _logger.info("{:<10d}{:<5s}{:<5s}{:<5s}".format(atom_idx+1, *freq_types[idx]))
            idx += 1

    # Zero point energy.
    _logger.info("")
    _logger.info("ZPE = {}".format(outcar.zpe))

