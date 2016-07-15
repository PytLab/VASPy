import sys

__version__ = '0.6.0'
__all__ = ['atomco', 'electro', 'iter', 'matstudio', 'plotter', 'incar']


class VasPy(object):
    def __init__(self, filename):
        "Base class to be inherited by all classes in VASPy."
        self.__filename = filename

    def filename(self):
        " Query function for bounded filename."
        return self.__filename


class CarfileValueError(Exception):
    "Exception raised for errors in the CONTCAR-like file."
    pass


class UnmatchedDataShape(Exception):
    "Exception raised for errors in unmatched data shape."
    pass

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')

# Compatible functions with py2 and py3.
if sys.version > "3":
    PY3 = True
else:
    PY3 = False


def listed_zip(*args):
    """
    A compatible version of `zip`.
    """
    if PY3:
        return list(zip(*args))
    else:
        return zip(*args)

