VASPy
========
[![Build Status](https://travis-ci.org/PytLab/VASPy.svg?branch=master)](https://travis-ci.org/PytLab/VASPy)
[![platform](https://img.shields.io/badge/python-2.6-green.svg)](https://www.python.org/download/releases/2.6.9/)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-2710/)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![versions](https://img.shields.io/badge/versions%20-%20%200.2.1-blue.svg)](https://github.com/PytLab/VASPy)

###An **object-oriented** VASP file processing library.

Make it **easier** to process VASP files.

处理VASP文件从未如此 **灵活** **简单**

命令行处理DOS文件使用举例：

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

处理ELFCAR举例:

    >>> from vaspy.electro import ElfCar
    >>> a = ElfCar() 
    >>> a.plot_contour()   # 绘制等高线图
    >>> a.plot_mcontour()  # 使用mlab绘制等高线图

绘制结果:

![](https://github.com/PytLab/VASPy/blob/dev/pic/contour2d.png)

![](https://github.com/PytLab/VASPy/blob/dev/pic/surface3d.png)

![](https://github.com/PytLab/VASPy/blob/dev/pic/mcontour3d.png)

使用者可以编写自己的脚本来批处理VASP文件

###更新日志
<table>
    <tbody>
        <tr>
            <td><strong>日期</strong></td>
            <td><strong>版本</strong></td>
            <td><strong>内容</strong></td>
        </tr>
        <tr>
            <td>2015-09-13</td>
            <td>0.2.1</td>
            <td>新增mlab绘制contour</td>
        </tr>
        <tr>
            <td>2015-09-13</td>
            <td>0.2.0</td>
            <td>新增ELFCAR图像绘制</td>
        </tr>
        <tr>
            <td>2015-09-12</td>
            <td>0.1.1</td>
            <td>新增d-band center计算</td>
        </tr>
        <tr>
            <td>2015-09-11</td>
            <td>0.1.0</td>
            <td>新增DosX类,处理分割后的DOS文件</td>
        </tr>
        <tr>
            <td>2015-09-10</td>
            <td>0.0.3</td>
            <td>新增OutCar类,提供分析原子的受力数据</td>
        </tr>
        <tr>
            <td>2015-08-11</td>
            <td>0.0.2</td>
            <td>新增XsdFile类,处理material studio的xsd文件</td>
        </tr>
        <tr>
            <td>2015-08-04</td>
            <td>0.0.1</td>
            <td>初始版本, 提供的功能:<br>
                <ul>
                1.处理cartisan坐标文件<br>
                2.处理POSCAR,CONTCAR文件中的数据<br>
                3.处理OSZAICAR，处理每步迭代数据<br>
                </ul>
            </td>
        </tr>
    </tbody>
</table>
