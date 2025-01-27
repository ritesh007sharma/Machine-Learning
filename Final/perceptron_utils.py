#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:27:48 2019

@author: ritesh
"""

import numpy as np
from threshold import *


mul = np.multiply
dot = np.dot
add = np.add

train_file = './data/data-splits/data.train'
test_file = './data/data-splits/data.test'
eval_file = './data/data-splits/data.eval.anon'
eval_nums_file = './data/data-splits/eval.id'

predict_out_file = './data/test_data/eval_out.csv'
predict_out_file_sum = './data/test_data/eval_out_sum.csv'


a_train = './data/test_data/a5a.train'
a_test = './data/test_data/a5a.test'
short_test = './data/test_data/short_test.test'


def evaluate_perceptron(testing_examples, weight_vector, theta=0):
    incorrect = 0
    total = 0
    act_pos = 0
    true_pos = 0
    pred_pos = 0
    prediction_array = []
    for example in testing_examples:
        ret = weight_vector * example - theta
        sign = -1 if ret < 0 else 1
        prediction_array.append(sign)
        if sign == 1 and example.label == 1:
            true_pos += 1
        if sign == 1:
            pred_pos += 1
        if example.label == 1:
            act_pos += 1
        if sign != example.label:
            incorrect += 1

        total += 1

    p = true_pos / pred_pos
    r = true_pos / act_pos
    fscore = 2 * p * r / (p + r)
#    print("f1 score: " + str(fscore))
#    print(incorrect)
#    print(prediction_array)
    return ((total - incorrect) / total), fscore, prediction_array

