import sys

if sys.version > "3":
    PY2 = False
else:
    PY2 = True


__version__ = '0.6.0'
__all__ = ['atomco', 'electro', 'iter', 'matstudio', 'plotter', 'incar']


class VasPy(object):
    def __init__(self, filename):
        "Base class to be inherited by all classes in VASPy."
        self.__filename = filename

    def filename(self):
        " Query function for bounded filename."
        return self.__filename

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

