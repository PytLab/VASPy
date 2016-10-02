#!/usr/bin/env python

from setuptools import setup, find_packages

from vaspy import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = "A pure Python library designed to make it easy and quick to manipulate VASP files"

long_description = """
=====
VASPy
=====

.. image:: https://travis-ci.org/PytLab/VASPy.svg?branch=master
    :target: https://travis-ci.org/PytLab/VASPy
    :alt: Build Status

.. image:: https://img.shields.io/badge/python-3.5-green.svg
    :target: https://www.python.org/downloads/release/python-351/
    :alt: platform

.. image:: https://img.shields.io/badge/python-2.7-green.svg
    :target: https://www.python.org/downloads/release/python-2710
    :alt: platform

.. image:: https://img.shields.io/github/stars/PytLab/VASPy.svg
    :target: https://github.com/PytLab/VASPy/stargazers

.. image:: https://img.shields.io/github/forks/PytLab/VASPy.svg
    :target: https://github.com/PytLab/VASPy/network


Introduction
------------

VASPy is a pure Python library designed to make it easy and quick to manipulate VASP files.

You can use VASPy to manipulate VASP files in command lins or write your own python scripts to process VASP files and visualize VASP data.

In `/scripts <https://github.com/PytLab/VASPy/tree/master/scripts>`_ , there are some scripts written by me for daily use.

Installation
------------
1. Via pip(recommend)::

    pip install vaspy

2. Via easy_install::

    easy_install vaspy

3. From source::

    python setup.py install

"""

install_requires = [
    'numpy>=1.11.1',
    'matplotlib>=1.5.2',
    'scipy>=0.18.0',
]

license = 'LICENSE'

# Get long description.
#with open("README.rst") as f:
#    lines = f.readlines()
#
#long_description = ""
#for line in lines:
#    if "Installation" in line:
#        break
#    else:
#        long_description += line

name = 'vaspy'
packages = [
    'vaspy',
]
platforms = ['linux']
url = 'https://github.com/PytLab/VASPy'
download_url = ''
classifiers = [
    'Development Status :: 3 - Alpha',
    'Topic :: Text Processing',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(author=author,
      author_email=author_email,
      description=description,
      license=license,
      long_description=long_description,
      install_requires=install_requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version,
      test_suite="tests",
      classifiers=classifiers)

