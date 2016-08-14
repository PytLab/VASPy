import logging

from vaspy.iter import OutCar

_logger = logging.getLogger("vaspy.script")

if "__main__" == __name__:
    outcar = OutCar()
    _logger.info("ZPE = {}".format(outcar.zpe))

