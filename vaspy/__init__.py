import logging
import sys

if sys.version > "3":
    PY2 = False
else:
    PY2 = True


__version__ = '0.7.3'
__all__ = ['atomco', 'electro', 'iter', 'matstudio', 'plotter', 'incar']


# Initialize logger.
logger = logging.getLogger("vaspy")
logger.setLevel(logging.INFO)
console_hdlr = logging.StreamHandler()
console_hdlr.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s   %(levelname)-8s %(message)s")
console_hdlr.setFormatter(formatter)
logger.addHandler(console_hdlr)


class VasPy(object):
    def __init__(self, filename):
        "Base class to be inherited by all classes in VASPy."
        self.filename = filename


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

