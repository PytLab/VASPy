__version__ = '0.0.2'


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
