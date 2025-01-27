#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:39:26 2019

@author: ritesh
"""

import math
from file_io import *


def get_threshold_one(train_set):
    threshold_arr = FeatureVector([0]*(360+1))
    for i in range(len(train_set)):
        for j in range(len(train_set[i].fv)):
            if train_set[i].fv[j] != 0:
                threshold_arr.fv[j] = 1
    return threshold_arr


def get_threshold_ig(train_set):
    threshold_arr = FeatureVector([0]*(360+1))
    for feature in range(len(train_set[0].fv)):
        sorted_arr = sorted(train_set, key=lambda s: s.fv[feature], reverse=True)
        threshold_arr.fv[feature] = get_ig_split(sorted_arr, feature)
        print(str(feature) + ':' + str(threshold_arr.fv[feature]))

    threshold_arr.fv = [1 if x == 0 else x for x in threshold_arr.fv]
    return threshold_arr


def get_ig_split(arr, feature):
    best_split = 0
    best_split_index = 0
    for example in range(len(arr)):
        split = evaluate_split(arr, example)
        if split > best_split:
            best_split = split
            best_split_index = example
        if arr[example].fv[feature] == 0:
            return arr[best_split_index].fv[feature]
    return arr[best_split_index].fv[feature]


def evaluate_split(arr, row):
    e_total = entropy(arr)
    low_split = arr[:row]
    high_split = arr[row:]
    rhs_sum = len(low_split)/len(arr) * entropy(low_split) + len(high_split)/len(arr) * entropy(high_split)
    return e_total - rhs_sum


def entropy(arr):
    if len(arr) == 0:
        return 0
    pos_count = 0
    for i in arr:
        if i.label == 1:
            pos_count += 1

    pos_count /= len(arr)
    neg_count = 1 - pos_count
    if pos_count == 0 and neg_count == 0:
        return 0
    if pos_count == 0:
        return -1 * neg_count * math.log2(neg_count)
    if neg_count == 0:
        return pos_count * (-1) * math.log2(pos_count)
    return pos_count * (-1) * math.log2(pos_count) - neg_count * math.log2(neg_count)