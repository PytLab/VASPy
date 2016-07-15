# -*- coding:utf-8 -*-
"""
========================================================================
Exception classes.
========================================================================
Written by PytLab <shaozhengjiang@gmail.com>, July 2016
Updated by PytLab <shaozhengjiang@gmail.com>, July 2016
========================================================================

"""


class CarfileValueError(Exception):
    "Exception raised for errors in the CONTCAR-like file."
    pass


class UnmatchedDataShape(Exception):
    "Exception raised for errors in unmatched data shape."
    pass

