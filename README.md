VASPy
========
[![Build Status](https://travis-ci.org/PytLab/VASPy.svg?branch=master)](https://travis-ci.org/PytLab/VASPy)
[![platform](https://img.shields.io/badge/python-2.6-green.svg)](https://www.python.org/download/releases/2.6.9/)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-2710/)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
<<<<<<< HEAD
![versions](https://img.shields.io/badge/versions%20-%20%200.0.3-blue.svg)
=======
[![versions](https://img.shields.io/badge/versions%20-%20%200.1.0-blue.svg)](https://github.com/PytLab/VASPy)
>>>>>>> dev

###An **object-oriented** VASP file processing library.

Make it **easier** to process VASP files.

处理VASP文件从未如此 **灵活** **简单**

命令行使用举例：

    #处理分割好的DOS文件
    >>> from vaspy.electro import DosX
    >>> a = DosX('DOS1')
    >>> b = DosX('DOS8')
    
    #分波态密度合并
    >>> c = a
    >>> c.reset_data()              # 初始化DOS数据
    >>> for i in xrange(1, 10):
    >>>    c += DosX('DOS'+str(i))  # 循环合并DOS数据
    >>> ...
    >>> c.data                      # 以float矩阵显示合并后的数据
                                    # 可直接进行计算等操作
    >>> c.tofile()                  # 生成新的合并后的DOS文件
    
    #绘图
    >>> c.plotsum(0, (5, 10))       # 绘制d轨道pDOS图
    
绘制结果:

![](https://github.com/PytLab/VASPy/blob/dev/pic/pDOS.png)
