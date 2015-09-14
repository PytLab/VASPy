#!/usr/bin/env python

from distutils.core import setup
from vaspy import __version__ as version

maintainer = 'Shao-Zheng-Jiang'
maintainer_email = 'shaozhengjiang@gmail.com'
author = maintainer
author_email = maintainer_email
description = __doc__

requires = [
    'numpy',
    'matplotlib'
]

license = 'LICENSE'
long_description = file('README.md').read()
name = 'python-vaspy'
packages = [
    'vaspy',
    'scripts',
    'unittest',
]
data_files = []
platforms = ['linux']
url = 'https://github.com/PytLab/VASPy'
download_url = ''

setup(
    author=author,
    author_email=author_email,
    description=description,
    license=license,
    long_description=long_description,
    maintainer=maintainer,
    name=name,
    packages=packages,
    data_files=data_files,
    platforms=platforms,
    url=url,
    download_url=download_url,
    version=version,
    )
