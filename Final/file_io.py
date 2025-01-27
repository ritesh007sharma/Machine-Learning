#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:39:53 2019

@author: ritesh
"""

import numpy as np


class FeatureTrans:
    fv = []
    label = 0

    def __init__(self, f_vector, lab=0):
        self.fv = f_vector
        self.label = lab if lab == 1 else -1

    def __mul__(self, rhs):
        if type(rhs) is FeatureTrans:
            return np.dot(self.fv, rhs.fv)
        elif type(rhs) is np.ndarray:
            return FeatureTrans(list(np.dot(self.fv, rhs)))
        elif type(rhs) is int:
            return np.multiply(self.fv, rhs)

    def __add__(self, rhs):
        if type(rhs) is FeatureTrans:
            return np.add(self.fv, rhs.fv)

    def __sub__(self, rhs):
        if type(rhs) is FeatureTrans:
            return FeatureTrans(list(np.subtract(self.fv, rhs.fv)))


def readFile(filename):
    line = []
    with open(filename) as f:
        for l in f:
            row = [0] * (360 + 1)
            s = l.split()

            for i in s[1:]:
                lval = i.split(':')
                if int(lval[0]) > 360:
                    print(lval[0])
                row[int(lval[0])] = int(lval[1])
                if int(lval[0]) < 1:
                    print(lval[0])

            line.append(FeatureTrans(row, int(s[0])))
    return line