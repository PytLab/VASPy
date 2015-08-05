# -*- coding:utf-8 -*-
"""
===============================================================================================
A XyzFile class which do operations on .xyz files.
===============================================================================================
Written by PytLab <shaozhengjiang@gmail.com>, November 2014
Updated by PytLab <shaozhengjiang@gmail.com>, August 2015

==============================================================

"""
import numpy as np
import math
from functions import *


class CarfileValueError(Exception):
    "Exception raised for errors in the CONTCAR-like file."
    pass


class XyzFile(object):
    """
    Create a OUT.ANI-like file class
    Data begins at 2nd line defaultly
    Example:

    >>> slab_xyz = XyzFile(filename='CONTCAR.xyz', data_begin=2, height=5.5, direction='z')

    Class attributes descriptions
    =======================================================================
      Attribute      Description
      ============  =======================================================
      filename       string, name of the file the direct coordiante data
                     stored in
      data_begin     int, the number of line from which the data begin
      height         float, the slab height
      direction      string, the direction the slab will move in
      contcar        string, CONTCAR templates file name including axes
                     informations
      new_order      boolean, if the instance has a new order of atom,
                     set new_order=True(False default)
      ============  =======================================================
    """
    def __init__(self, filename, contcar='CONTCAR',
                 data_begin=2, height=0.0, direction='z'):
        self.filename = filename
        self.data_begin_int = int(data_begin)
        self.slab_height = float(height)
        self.operation_axis = direction
        self.contcar = contcar
        #self.new_order = new_order
        self.atom_dict = self.get_atom_info()
        self.atom_order_list = self.get_atom_order()
        self.axes = self.get_axes(contcar)
        self.content_str = self.get_data_string()
        self.content_list = self.get_data_list()
        self.pure_data_array = self.get_pure_data()
        self.atom_type_num = len(self.atom_dict)
        self.atomco_dict = self.get_atomco_dict()

    def get_atomco_dict(self):
        """
        Return a dict store atom type and coordinates.
        {string : list of list of string}
        Example:
        >>> a.atomco_dict
        >>> {'C' : [['2.01115823704755', '2.33265069974919', '10.54948252493041']],
             'Co': [['0.28355818414485', '2.31976779057375', '2.34330019781397'],
                    ['2.76900337448991', '0.88479534087197', '2.34330019781397']]}
        """
        atomtype_num_dict = {}
        #atom_coord_list = []
        for line_list in self.content_list:
            if not line_list[0] in atomtype_num_dict:
                atom_coord_list = []
                atom_coord_list.append(line_list[1:4])
                atomtype_num_dict[line_list[0]] = atom_coord_list
            else:
                atomtype_num_dict[line_list[0]].append(line_list[1:4])
        return atomtype_num_dict

    def get_axes(self, contcar):
        axis_list = []
        try:
            file_obj = open(contcar, 'rU')
        except:
            print "Failed to read CONTCAR! Input other filename or check it!"
        for i in range(2):
            file_obj.readline()
        for i in range(3):
            line_list = str2list(file_obj.readline())
            axis_list.append(line_list)
        file_obj.close()
        #convert axis list to matrix
        return np.float64(np.array(axis_list))

    def get_atom_order(self):
        """
        Return a list of string.
        """
        ##if not self.new_order:  #read atom order in CONTCAR-like file.
            ##file_obj = open(self.contcar, 'rU')
            ##for i in range(5):
                ##line = file_obj.readline()
            ##atom_order_str = file_obj.readline()
            ##atom_order_list = str2list(atom_order_str)
            ##file_obj.close()
        ##else:  #egt atom_order_list from atom_dict
        return [x for x in self.atom_dict]

        #return atom_order_list

    def change_direction(self, new_axis):
        """return new operation axis of the instance."""
        self.operation_axis = new_axis
        return self.operation_axis

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        info_str = ('filename:' + self.filename + '\n' +
                    'operation direction : %s\n' % (self.operation_axis) +
                    'slab height : %f\n' % (self.slab_height) +
                    '='*23 + '\n' +
                    '%5s : %5s\n' % ('atom', 'number'))
        for key in self.atom_dict:
            info_str += "%5s : %5s\n" % (key, str(self.atom_dict[key]))
        #get axes info
        info_str += ('='*66 + '\n' +
                     'xyz:\n' +
                     array2str(self.axes) +
                     '='*66)
        return info_str

    def get_data_string(self):
        """
        Return the data content in string format.
        """
        file_obj = open(self.filename, 'rU')
        for i in range(self.data_begin_int):  # read 2 lines
            file_obj.readline()
        content_str = ''
        for line_str in file_obj:
            line_list = str2list(line_str)
            content_str += '%5s%25.16f%25.16f%25.16f\n' % \
                           (tuple([line_list[0]]) + tuple([float(x) for x in line_list[1:4]]))
        #content_str = file_obj.read()
        file_obj.close()
        #self.content_str = content_str
        return content_str

    def get_data_list(self):
        """Return data in list."""
        file_obj = open(self.filename, 'rU')
        for i in range(self.data_begin_int):  # read 2 lines
            file_obj.readline()
        content_list = []
        for line_str in file_obj:
            line_list = str2list(line_str)  # strip whitespace in datalist
            content_list.append(line_list)
        #self.content_list = content_list
#        print "%s --> available" % ('data list')
        return content_list

    def get_data_array(self):
        "Return data in np.array, dtype = np.string."
        self.data_array = np.array(self.content_list)
#        print "%s --> available" % ('data array')
        return self.data_array

    def get_pure_data(self):
        "return pure data in np.array(dtype=np.float64)."
        pure_data_array = np.float64(self.get_data_array()[:, 1:4])
        return pure_data_array

    def translate_slab(self, value, axis):
        """
        Add certain value to certain axis of data.
        Return a new pure_data_array.
        Example:
        instance.add_slab(10.0, 'z')
        """
        pure_data_array = self.pure_data_array
        array_shape_tup = pure_data_array.shape
        slab_value = np.float64(value)
        #get a matrix to be added
        #use matrix multipication to broadcast ndarray
        if axis == 'x':
            added_array = np.outer(np.ones(array_shape_tup[0], dtype=np.float64),
                                   np.array([1.0, 0.0, 0.0], dtype=np.float64)*slab_value)
        elif axis == 'y':
            added_array = np.outer(np.ones(array_shape_tup[0], dtype=np.float64),
                                   np.array([0.0, 1.0, 0.0], dtype=np.float64)*slab_value)
        elif axis == 'z':
            added_array = np.outer(np.ones(array_shape_tup[0], dtype=np.float64),
                                   np.array([0.0, 0.0, 1.0], dtype=np.float64)*slab_value)

        #update attribute value
        #update self.pure_data_array
        self.pure_data_array = pure_data_array + added_array
        self.update_data()
        return self.pure_data_array

    def update_data(self):
        """
        Update attributes(self.content_str, self.content_list, self.pure_data_array)
        value after add a slab value.
        """
        #update self.pure_data_array
        #Oops! It has been updated already~
        #update self.content_list
        updated_content_list = []
        for i in xrange(len(self.content_list)):
            #get the atom type string
            atom_str = [self.content_list[i][0]]
            #get coordinates value
            atom_coord = list(self.pure_data_array[i].astype('|S32'))
            updated_content_list.append(atom_str + atom_coord)
        self.content_list = updated_content_list
        #update self.content_str
        updated_content_str = ''
        for atom_list in self.content_list:
            #updated_content_str += '%5s%25s%25s%25s\n' % tuple(atom_list)
            updated_content_str += '%5s%25.16f%25.16f%25.16f\n' % \
                                   (tuple([atom_list[0]]) + tuple([float(x) for x in atom_list[1:4]]))
        self.content_str = updated_content_str
#        print '%s --> updated' % ("data in instance")
        #return None

    def get_atom_info(self):
        """
        Return a dictionary contains infomation about atom type and number.
        Example:
        {'O':32, 'C':24}
        """
        file_obj = open(self.filename, 'rU')
        for i in range(self.data_begin_int):
            file_obj.readline()
        #count atom number and type
        ##atom_compared = ''
        atom_dict = {}
        for line_str in file_obj:
            line_list = str2list(line_str)
            atom_type = line_list[0]
            if not atom_type in atom_dict:
                ##atom_compared = atom_type
                ##atom_count = 1
                atom_dict[atom_type] = 1
            else:
                ##atom_count += 1
                atom_dict[atom_type] += 1
        file_obj.close
#        print "%s --> available" % ('atom infomation')
        return atom_dict

    def axis_map(self,  axis_tuple=((1.0, 0.0, 0.0),
                                    (0.0, 1.0, 0.0),
                                    (0.0, 0.0, 1.0))):
        """
        Map the self.pure_data_array/coordinates matrix to
        new data array in new axis space.
        Default axis = ((1.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, 0.0, 1.0)).
        Return a new atom coordinates array.
        """
        #if you want to understand the code below,
        #i believe you should do some matrix operation on your paper ^_^

        #initialize axis mol matrix
        axis_mol_matrix = np.matrix([1.0, 1.0, 1.0], dtype=np.float64)
        #get new axis from axis_tuple
        axis_matrix = np.matrix(axis_tuple, dtype=np.float64)
        #use matrix dot multipication to get dotted coordinates in new axis_tuple
        dotted_data_matrix = np.matrix(self.pure_data_array)*axis_matrix.T
        #get axis mol matrix
        for i in range(3):
            mol_float = math.sqrt(axis_matrix[i, 0]**2 +
                                  axis_matrix[i, 1]**2 +
                                  axis_matrix[i, 2]**2)
            axis_mol_matrix[:, i] = mol_float
        #get coordiante value after mapping
        #this part use multipication of np.array instead of matrix
        axis_mol_array = np.array(axis_mol_matrix)
        dotted_data_array = np.array(dotted_data_matrix)
        mapped_data_array = dotted_data_array * (1/axis_mol_array)

        return mapped_data_array

    def convert_axis(self,
                     axis_tuple=((1.0, 0.0, 0.0),
                                 (0.0, 1.0, 0.0),
                                 (0.0, 0.0, 1.0)),
                     contcar=None):
        """
        Expect a set of new axis array(use tuple as input).
        Return a new points coordinates array
        Default axis : ((1.0, 0.0, 0.0),(0.0, 1.0, 0.0),(0.0, 0.0, 1.0)).
        If a CONTCAR-like file is provided, read new axis in CONTCAR-like file.
        """
        #get new axis matrix
        if contcar is None:
            axis_array = np.array(axis_tuple, dtype=np.float64)
        else:
            axis_list = []
            file_obj = open(contcar, 'rU')
            for i in range(2):
                file_obj.readline()
            for i in range(3):
                line_list = str2list(file_obj.readline())
                axis_list.append(line_list)
            file_obj.close()
            #convert axis list to matrix
            axis_array = np.float64(np.array(axis_list))

        #do axis convertion
        def get_new_coordinate(old_point_vector, new_axis_array):
            #get new coordinates of point in new coordinates axis
            new_axis_matrixI = np.matrix(new_axis_array).I
            return list(np.dot(old_point_vector, new_axis_matrixI))
        #use list comprehension instead of "for loop"
        old_data_array = self.pure_data_array
        new_data_array = np.array([get_new_coordinate(point_vector, axis_array)
                                   for point_vector in old_data_array])

        return np.array(new_data_array).reshape(-1, 3)  # turn 4-D array into 2-D array

    def change_axes(self, new_axis_tuple):
        """
        Change the axes of the instance.
        """
        self.axes = np.array(new_axis_tuple, dtype=np.float64)
#        print "Axes --> updated!"

    def __add__(self, xyzFile_inst):
        """
        Add 2 xyzFile, return a new xyzFile_inst.
        The second instance is the slab at the bottom.
        """
        if self.operation_axis == xyzFile_inst.operation_axis:
            #create a new CONTCAR.xyz-like file
            #height of the above slab + that of the below one
            self.translate_slab(xyzFile_inst.slab_height, self.operation_axis)
            #add atom data below too above slab
            new_atomco_dict = combine_atomco_dict(self.atomco_dict,
                                                  xyzFile_inst.atomco_dict)
            ##new_content_str = self.content_str + \
                              ##xyzFile_inst.content_str
            new_content_str = atomdict2str(new_atomco_dict)
            #get number of atom
            atom_num = sum([x for x in self.atom_dict.values()]) + \
                       sum([y for y in xyzFile_inst.atom_dict.values()])
            newfile_name = self.filename.split('.')[0] + 'plus' + \
                           xyzFile_inst.filename.split('.')[0] + '.xyz'
            newslab_height_float = self.slab_height + xyzFile_inst.slab_height
            #create a new file
            towrite_list = ['atom number : %d\n' % (atom_num),
                            'created by atomco designed by Pytlab\n',
                            new_content_str]
            file_obj = open(newfile_name, 'w')
            for content_str in towrite_list:
                file_obj.write(content_str)
            file_obj.close()
#            print "%s  --> created" % ('new instance')
#            print "file %s --> created" % (newfile_name)

            return XyzFile(filename=newfile_name, data_begin=2,
                           height=newslab_height_float,
                           direction=self.operation_axis)
        else:
            raise AttributeError('Axis of two instance is different! Check it again!')

    def creat_contcar_file(self, filename='CONTCAR_comb'):
        """
        Create a CONTCAR-like file in current diractory.
        Return the file's name in string.
        """
        content_str = ''
        #get atom info
        atom_info_str = 'xyz '
        atom_info_str = atom_info_str + ' '.join(self.atom_dict.keys()) + '\n'
        #second line scaling
        scaling_str = ' '*3 + '1.00000000000000\n'
        content_str = content_str + atom_info_str + scaling_str
        #axes
        for axis_array in self.axes:
            content_str += '%22.16f%22.16f%22.16f\n' % tuple(axis_array)
        #atom type and number
        atom_type_str = ' '*3 + \
                        '%-5s'*self.atom_type_num % tuple(self.atom_order_list) +\
                        '\n'
        #get atom number tuple
        atom_number_tup = tuple([self.atom_dict[x] for x in self.atom_order_list])
        atom_num_str = ' '*3 + \
                       '%-5d'*self.atom_type_num % atom_number_tup +\
                       '\n'
        content_str = (content_str + atom_type_str + atom_num_str +
                       'Selective dynamics\nDirect\n')
        #relative coordinates
        #get relative coordinates array
        rel_coord_array = self.convert_axis(axis_tuple=self.axes)
        #get T and F list
        data, tfs = self.get_contcar_data(self.contcar)
        #get content string
        if tfs:  # if T and F info setted
            if len(tfs) != len(rel_coord_array):
                raise CarfileValueError('Different atom number in %s' % self.contcar)
            for coord_array, tf in zip(rel_coord_array, tfs):
                newline = '%22.18f%22.18f%22.18f%5s%5s%5s\n' % \
                          tuple(list(coord_array) + tf)
                content_str += newline
        else:  # no T and F
            for coord_array in rel_coord_array:
                content_str += '%22.18f%22.18f%22.18f\n' % tuple(coord_array)

        #write into file
        file_obj = open(filename, 'w')
        file_obj.write(content_str)
        file_obj.close()
#        print "%s --> created" % (filename)

    #Add on 2015-08-03
    @staticmethod
    def get_contcar_data(contcar):
        "Read contcar-like file to get data and TF info."
        with open(contcar, 'r') as f:
            for i in xrange(9):
                f.readline()
            data, tf = [], []  # data and T or F info
            for line_str in f:
                line_list = str2list(line_str)
                data.append(line_list[:3])
                if len(line_list) > 3:
                    tf.append(line_list[3:])

        return data, tf


class PosCar(object):
    def __init__(self, filename):
        """
        Class to generate POSCAR or CONTCAR-like objects.
        """
        self.filename = filename
        #load all data in file
        self.load()

    def load(self):
        "Load all information in POSCAR."
        with open(self.filename, 'r') as f:
            content_list = f.readlines()
            #get scale factor
            axes_coeff = float(content_list[1])
            #axes
            axes = [str2list(axis) for axis in content_list[2:5]]
            #atom info
            atoms = str2list(content_list[5])
            natoms = str2list(content_list[6])  # atom number
            #data
            data, tf = [], []  # data and T or F info
            for line_str in content_list[9:]:
                line_list = str2list(line_str)
                data.append(line_list[:3])
                if len(line_list) > 3:
                    tf.append(line_list[3:])
        #data type convertion
        axes = np.float64(np.array(axes))  # to float
        natoms = [int(i) for i in natoms]
        data = np.float64(np.array(data))

        #set class attrs
        self.axes_coeff = axes_coeff
        self.axes = axes
        self.atoms = zip(atoms, natoms)
        self.data = data
        self.tf = tf

        return

    def __repr__(self):
        with open(self.filename, 'r') as f:
            content = f.read()
        return content

    def __str__(self):
        return self.__repr__()
