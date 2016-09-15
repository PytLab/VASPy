#!/usr/bin/env python

from setuptools import setup, find_packages

from vaspy import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = "A pure Python library designed to make it easy and quick to manipulate VASP files"

requires = [
    'numpy>=1.11.1',
    'matplotlib>=1.5.2',
    'scipy>=0.18.0',
]

license = 'LICENSE'

# Get long description.
with open("README.rst") as f:
    lines = f.readlines()

long_description = ""
for line in lines:
    if "Installation" in line:
        break
    else:
        long_description += line

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
      setup_requires=requires,
      maintainer=maintainer,
      name=name,
      packages=find_packages(),
      package_data=package_data,
      platforms=platforms,
      url=url,
      download_url=download_url,
      version=version,
      test_suite="tests",
      classifiers=classifiers)

