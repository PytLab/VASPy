__version__ = '0.4.3'
__all__ = ['atomco', 'electro', 'iter', 'matstudio', 'plotter']


class VasPy(object):
    def __init__(self, filename):
        "Base class to be inherited by all classes in VASPy."
        self.filename = filename


class CarfileValueError(Exception):
    "Exception raised for errors in the CONTCAR-like file."
    pass


class UnmatchedDataShape(Exception):
    "Exception raised for errors in unmatched data shape."
    pass

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')
