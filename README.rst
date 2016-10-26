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

.. image:: https://img.shields.io/badge/pypi-v0.7.10-blue.svg
    :target: https://pypi.python.org/pypi/vaspy/
    :alt: versions

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

Examples
--------

manipulate splited DOS file in command-line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # 处理分割好的DOS文件
    >>> from vaspy.electro import DosX
    >>> a = DosX('DOS1')
    >>> b = DosX('DOS8')
    
    # 分波态密度合并
    >>> c = a
    >>> c.reset_data()              # 初始化DOS数据
    >>> for i in xrange(1, 10):
    >>>    c += DosX('DOS'+str(i))  # 循环合并DOS数据
    >>> ...
    >>> c.data                      # 以float矩阵显示合并后的数据
                                    # 可直接进行计算等操作
    >>> c.tofile()                  # 生成新的合并后的DOS文件
    
    # 绘图
    >>> c.plotsum(0, (5, 10))       # 绘制d轨道pDOS图

**Output**

.. image:: https://github.com/PytLab/VASPy/blob/dev/pic/pDOS.png

Visualize ELFCAR
~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from vaspy.electro import ElfCar
    >>> a = ElfCar() 
    >>> a.plot_contour()   # 绘制等值线图
    >>> a.plot_mcontour()  # 使用mlab绘制等值线图(需安装Mayavi)
    >>> a.plot_contour3d() # 绘制3d等值线图
    >>> a.plot_field()     # 绘制标量场

**Output**

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/contour2d.png

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/contours.png

**3D contour**

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/contour3d.png

**Scalar field**

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/field.png

Charge difference (Use ChgCar class)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/contourf.png

Manipulate XDATCAR:
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from vaspy.atomco import XdatCar
    >>> xdatcar = XdatCar()
    >>> # 输出xdatcar相应Cartesian坐标
    >>> for step, data in xdatcar:
    >>>     print step
    >>>     print xdatcar.dir2cart(xdatcar.bases, data)
    >>> # 可直接运行script/中脚本生成相应.arc文件用于MaterialStudio显示动画
    >>> python xdatcar_to_arc.py

**animation**

.. image:: https://github.com/PytLab/VASPy/blob/master/pic/sn2_my.gif

**You can write your OWN script to process VASP files**

From author
-----------
Welcome to use **VASPy**  (●'◡'●)ﾉ♥

- If you find any bug, please report it to me by open a issue.
- **VASPy** needs to be improved, your contribution will be welcomed.

Important update log
--------------------

.. csv-table::
    :header: "Date", "Version", "Description"

    "2016-08-08", "0.7.0", "增强库的通用性"
    "2016-07-15", "0.6.0", "兼容python 3"
    "2015-08-04", "0.1.0", "初始版本"

