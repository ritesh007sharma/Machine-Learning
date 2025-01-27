#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 22:54:08 2019

@author: ritesh
"""

import numpy as np
    
def sign(input):
    output = input.copy()
        
    output[output>=0] = 1
    output[output<0] = -1
    
    return output
    
class Perceptron(object):
    def __init__(self, dim = 0, avg_flag = False, pocket_flag = False):
        self.dim = dim + 1;
        self.w = np.zeros(self.dim)
        self.wp = np.zeros(self.dim)
        self.w_avg = np.zeros(self.dim)
        self.avg_flag = avg_flag
        self.pocket_flag = pocket_flag
        self.cnt = 0
        self.current_counter = 0
        self.pocket_counter = 0
    
    def init_random(self):
        self.w = 0.02 * np.random.rand(self.dim) - 0.01
        self.w_avg = self.w.copy()
        
    def update(self, lr, x, y):
        self.w = self.w + lr * y * np.append(x, 1)
    
        
    def updateAvg(self):
        self.cnt += 1
        if(self.avg_flag == True):
            alpha = float(1)/self.cnt
            self.w_avg = (1 - alpha) * self.w_avg + alpha * self.w
    
    def predict(self, x):
        if(self.avg_flag == False):
            if(x.ndim == 1):
                return sign(np.array([self.w.dot(np.append(x,1))]))
            else:
                return sign(np.append(x,np.ones([len(x), 1]), 1).dot(self.w.T))
        
        elif(self.pocket_flag == True):
            if(x.ndim == 1):
                return sign(np.array([self.wp.dot(np.append(x,1))]))
            else:
                return sign(np.append(x,np.ones([len(x), 1]), 1).dot(self.wp.T))
            
        else:
            if(x.ndim == 1):
                return sign(np.array([self.w_avg.dot(np.append(x,1))]))
            else:
                return sign(np.append(x, np.ones([len(x),1]),1).dot(self.w_avg.T))
            
            
            
    def predictTrain(self, x):
        if(x.ndim == 1):
            return sign(np.array([self.w.dot(np.append(x,1))]))
        else:
            return sign(np.append(x, np.ones([len(x), 1]), 1).dot(self.w.T))