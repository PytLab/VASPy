# -*- coding:utf-8 -*-

import string

import numpy as np


def str2list(rawstr):
    rawlist = rawstr.strip(string.whitespace).split(' ')
    # Remove space elements in list.
    cleanlist = [x for x in rawlist if x != ' ' and x != '']
    return cleanlist


def line2list(line, field=' ', dtype=float):
    "Convert text data in a line to data object list."
    strlist = line.strip().split(field)
    if type(dtype) != type:
        raise TypeError('Illegal dtype.')
    datalist = [dtype(i) for i in strlist if i != '']

    return datalist


def array2str(raw_array):
    """
    convert 2d array -> string
    """
    array_str = ''
    for array_1d in raw_array:
        array_str += '(%-20.16f, %-20.16f, %-20.16f)\n' % (tuple(array_1d))

    return array_str


def combine_atomco_dict(dict_1, dict_2):
    """
    Combine 2 dict of atomco_dict.
    Return a new combined dict.
    >>> a.atomco_dict
    >>> {'C': [['2.01115823704755', '2.33265069974919', '10.54948252493041']],
         'Co': [['0.28355818414485', '2.31976779057375', '2.34330019781397'],
                ['2.76900337448991', '0.88479534087197', '2.34330019781397']]}
    """
    new_atomco_dict = {}
    for atom_type_str in dict_1:
        if atom_type_str in dict_2:
            new_atomco_dict[atom_type_str] = dict_1[atom_type_str] + \
                                             dict_2[atom_type_str]
        else:
            new_atomco_dict[atom_type_str] = dict_1[atom_type_str]
    for atom_type_str in dict_2:
        if atom_type_str in dict_1:
            pass
        else:
            new_atomco_dict[atom_type_str] = dict_2[atom_type_str]

    return new_atomco_dict


def atomdict2str(atomco_dict, keys):
    """
    Convert atomco_dict to content_str.
    from
    {'C' : [[2.01115823704755, 2.33265069974919, 10.54948252493041]],
     'Co': [[0.28355818414485, 2.31976779057375, 2.34330019781397],
            [2.76900337448991, 0.88479534087197, 2.34330019781397]]}
    to
    'C   2.01115823704755   2.33265069974919   10.54948252493041\n
     Co  0.28355818414485   2.31976779057375   2.34330019781397 \n
     Co  2.76900337448991   0.88479534087197   2.34330019781397 \n'
    """
    content_str = ''
    for atom in keys:
        n = len(atomco_dict[atom])
        for i in range(n):
            data = [atom] + atomco_dict[atom][i]
            content_str += '{:<3s}{:>16.7f}{:>16.7f}{:>16.7f}\n'.format(*data)

    return content_str


def get_combinations(x, y, z):
    "get all combiantions 0~x, 0~y, 0~z, then zip it"
    combinations = []
    for i in np.linspace(0, 10, z):
        for j in np.linspace(0, 10, y):
            for k in np.linspace(0, 10, x):
                combinations.append((k, j, i))
    xyz = zip(*combinations)
    xyz = np.array(xyz)
    return xyz


def get_angle(v1, v2):
    "Get included angle of vectors v1 and v2."
    l1, l2 = np.linalg.norm(v1), np.linalg.norm(v2)
    cos_angle = np.dot(v1, v2)/(l1*l2)
    angle = np.arccos(cos_angle)*180/np.pi

    return angle

