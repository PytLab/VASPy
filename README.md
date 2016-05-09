 VASPy
========
[![Build Status](https://travis-ci.org/PytLab/VASPy.svg?branch=master)](https://travis-ci.org/PytLab/VASPy)
[![platform](https://img.shields.io/badge/python-2.6-green.svg)](https://www.python.org/download/releases/2.6.9/)
[![platform](https://img.shields.io/badge/python-2.7-green.svg)](https://www.python.org/downloads/release/python-2710/)
[![Software License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![versions](https://img.shields.io/badge/versions%20-%20%200.5.5-blue.svg)](https://github.com/PytLab/VASPy)

### An **object-oriented** VASP file processing library.

Make it **easier** to process VASP files.

处理VASP文件从未如此 **灵活** **简单**

---

***VASPy*** 是一个纯python编写的处理VASP文件的框架

使用者可以使用***VASPy***的接口简单快捷的编写处理VASP文件的脚本，也可以在命令行直接操作VASP文件。

[`/scripts`](https://github.com/PytLab/VASPy/tree/master/scripts)下是本人根据自己的需求，使用VASPy所写的一些脚本，可作为参考。

---

### 命令行处理DOS文件使用举例：

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
    
#### 绘制结果:

![](https://github.com/PytLab/VASPy/blob/dev/pic/pDOS.png)

处理ELFCAR举例:

    >>> from vaspy.electro import ElfCar
    >>> a = ElfCar() 
    >>> a.plot_contour()   # 绘制等值线图
    >>> a.plot_mcontour()  # 使用mlab绘制等值线图(需安装Mayavi)
    >>> a.plot_contour3d() # 绘制3d等值线图
    >>> a.plot_field()     # 绘制标量场

#### 绘制结果:

![](https://github.com/PytLab/VASPy/blob/master/pic/contour2d.png)

![](https://github.com/PytLab/VASPy/blob/master/pic/contours.png)

3D 等值线图

![](https://github.com/PytLab/VASPy/blob/master/pic/contour3d.png)

scalar field

![](https://github.com/PytLab/VASPy/blob/master/pic/field.png)

charge difference(use ChgCar class)

![](https://github.com/PytLab/VASPy/blob/master/pic/contourf.png)

操作XDATCAR举例

    >>> from vaspy.atomco import XdatCar
    >>> xdatcar = XdatCar()
    >>> # 输出xdatcar相应Cartesian坐标
    >>> for step, data in xdatcar:
    >>>     print step
    >>>     print xdatcar.dir2cart(xdatcar.bases, data)
    >>> # 可直接运行script/中脚本生成相应.arc文件用于MaterialStudio显示动画
    >>> python xdatcar_to_arc.py

动画实例

![](https://github.com/PytLab/VASPy/blob/master/pic/sn2_my.gif)

**使用者可以编写自己的脚本来批处理VASP文件**

### 重要更新日志
<table>
    <tbody>
        <tr>
            <td><strong>日期</strong></td>
            <td><strong>版本</strong></td>
            <td><strong>内容</strong></td>
        </tr>
        <tr>
            <td>2015-11-17</td>
            <td>0.4.1</td>
            <td>XdatCar类实现迭代协议</td>
        </tr>
        <tr>
            <td>2015-10-09</td>
            <td>0.3.0</td>
            <td>新增InCar类</td>
        </tr>
        <tr>
            <td>2015-10-07</td>
            <td>0.2.12</td>
            <td>新增Dos图颜色填充和dband center显示</td>
        </tr>
        <tr>
            <td>2015-09-30</td>
            <td>0.2.11</td>
            <td>新增修改xsd文件中特定原子颜色的方法</td>
        </tr>
        <tr>
            <td>2015-09-22</td>
            <td>0.2.10</td>
            <td>新增绘制TOTAL-FORCE曲线的脚本</td>
        </tr>
        <tr>
            <td>2015-09-19</td>
            <td>0.2.7</td>
            <td>ELFCAR等值线绘制支持空间扩展</td>
        </tr>
        <tr>
            <td>2015-09-17</td>
            <td>0.2.5</td>
            <td>新增ContCar类</td>
        </tr>
        <tr>
            <td>2015-09-16</td>
            <td>0.2.4</td>
            <td>新增利用VASPy所写的生成VASP输入文件的脚本<br>以及由CONTAR生成xsd文件的脚本</td>
        </tr>
        <tr>
            <td>2015-09-15</td>
            <td>0.2.3</td>
            <td>修复XsdFile类中数据顺序与POSCAR中顺序冲突的bug</td>
        </tr>
        <tr>
            <td>2015-09-15</td>
            <td>0.2.2</td>
            <td>新增3d等值线图和标量场绘制</td>
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
                3.处理OSZICAR，处理每步迭代数据<br>
                </ul>
            </td>
        </tr>
    </tbody>
</table>
