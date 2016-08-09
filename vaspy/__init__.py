import sys

if sys.version > "3":
    PY2 = False
else:
    PY2 = True


__version__ = '0.7.0'
__all__ = ['atomco', 'electro', 'iter', 'matstudio', 'plotter', 'incar']


class VasPy(object):
    def __init__(self, filename):
        "Base class to be inherited by all classes in VASPy."
        self.filename = filename

import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M:%S')


class LazyProperty(object):
    """
    Descriptor for lazy property.
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val

