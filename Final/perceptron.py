#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 20:26:05 2019

@author: ritesh
"""

import random
import numpy as np

trainFile = './data/data-splits/data.train'
testFile = './data/data-splits/data.test'
evalFile = './data/data-splits/data.eval.anon'
evanNumsFile = './data/data-splits/eval.id'
outputFile = './data/test_data/evalOut.csv'



thresholdArr = FeatureTrans([0, 2, 47, 0, 0, 0, 0, 0, 0, 1, 0, 299, 0, 0, 2, 6, 0, 0, 0, 0, 0, 20744, 0, 0, 44, 1100, 25,
                           0, 0, 0, 152, 6, 0, 6, 0, 79, 0, 3478, 0, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           306, 15, 0, 0, 0, 0, 0, 0, 0, 0, 1096, 0, 0, 0, 2, 0, 1, 0, 8988, 0, 0, 0, 0, 0, 0, 8, 0, 32,
                           0, 9, 0, 9, 0, 9, 0, 0, 0, 0, 8, 0, 2607, 0, 8, 81, 0, 0, 0, 0, 1, 2, 0, 2, 5, 314, 1917, 0,
                           2454, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3818, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                           0, 0, 0, 30, 0, 0, 0, 79, 0, 0, 11, 552, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 390, 0, 0, 0, 1631, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 303, 0, 16, 0, 0, 0, 0, 0, 0, 0, 855, 0, 0, 0, 0, 0, 1, 0, 0,
                           1, 0, 41, 92, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 0, 0, 0, 1841, 0, 0, 0, 0, 0, 0, 7233, 0, 2, 0,
                           0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 2, 0, 0, 0, 0, 41, 41, 0, 0, 0, 178, 3, 0, 0, 0, 0, 1,
                           1, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40,
                           0, 0, 0, 0, 0, 54, 3, 50, 0, 0, 0, 0, 665, 15, 1, 48, 0, 4, 0, 0, 0, 113, 0, 1, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1544, 285])

thresholdArrOne = FeatureTrans([1 if x == 0 else x for x in thresholdArr.fv[:]])

def preProcess(trainSet, thresholdArr):
    for i in range(len(trainSet)):
        for j in range(len(trainSet[i].fv)):
            if trainSet[i].fv[j] <= thresholdArr.fv[j]:
                trainSet[i].fv[j] = 0
            else:
                trainSet[i].fv[j] = 1

    return trainSet

def evalPerceptron(testExamples, wVec, theta=0):
    wrong = 0
    total = 0
    actualPos = 0
    truePos = 0
    predPos = 0
    arr = []
    for example in testExamples:
        result = wVec * example - theta
        if result < 0:
            sign = -1
        else:
            sign = 1
        arr.append(sign)
        if sign == 1 and example.label == 1:
            truePos += 1
        if sign == 1:
            predPos += 1
        if example.label == 1:
            actualPos += 1
        if sign != example.label:
            wrong += 1

        total += 1

    p = truePos / predPos
    r = truePos / actualPos
    fscore = 2 * p * r / (p + r)
    return ((total - wrong) / total), fscore, arr



def perceptron(trainingExamples, w, a, r=1.0, mew=0.0):
    for example in trainingExamples:
        correct = example.label * (example * w)
        if correct <= mew:
            w.fv += example * example.label * r
        a.fv = a + w

    return w, a



def crossValidation(trainFile, testFile, numEpoch=1, average=False, runFunc=None, trainThreshold=None):
    epochArr = [1, 2, 3, 5, 7, 9]
    nuArr = [0, 0.1, 0.5, 1, 2, 3, 4, 5, 7, 9, 12]
    rArr = [0.05, 0.07, 0.1, 0.5, 1.0, 2.0]
    maxVal = 0

    trainSet = readFile(trainFile)
    testSet = readFile(testFile)
    if runFunc or trainThreshold:
        if runFunc:
            trainThreshold = runFunc(trainSet)
            wVec = FeatureTrans(trainThreshold.fv[:])
        else:
            wVec = FeatureTrans([0]*(360+1))

        preProcess(trainSet, trainThreshold)
        preProcess(testSet, trainThreshold)

    else:
        wVec = FeatureTrans([0]*(360+1))

    wVec.fv[0] = 1
    avgVec = FeatureTrans([0]*(360+1))
    avgVec.fv[0] = 1
    maxScore = [0, 0, 0, 0]
    for l in range(len(epochArr)):
        for i in range(len(nuArr)):
            for j in range(len(rArr)):
                if not trainThreshold:
                    wVec = FeatureTrans(trainThreshold.fv[:])
                    wVec.fv[0] = 1
                else:
                    wVec = FeatureTrans([0]*(360+1))

                avgVec = FeatureTrans([0]*(360+1))
                avgVec.fv[0] = 1
#                print('epoch count: ' + str(epochArr[l]) + ' - mew: ' + str(nuArr[i]) + ' - r: ' + str(rArr[j]))
                for k in range(epochArr[l]):
                    wVec, avgVec = perceptron(trainSet, wVec, avgVec, mew=nuArr[i], r=rArr[j])
                if average:
                    correctPercent, fscore, arr = evalPerceptron(testSet, avgVec)
                else:
                    correctPercent, fscore, arr = evalPerceptron(testSet, wVec)
#                print('fscore: ' + str(fscore) + '\n')
                maxVal = max(maxVal, fscore)
                # print("percent: " + str(correctPercent) + '\n')
                if fscore > maxScore[0]:
                    maxScore = [fscore, nuArr[i], rArr[j], epochArr[l]]
            # numEpoch += 1
   
    #print('\n\nmax fscore: {0} with mew {1}, r {2}, epochs: {3}'.format(maxScore[0], maxScore[1], maxScore[2], maxScore[3]))

    print(maxVal)

def calculateOne(trainFile, testFile, numEpoch=1, average=False, runFunc=None, thresh_arr=None,
                           mew=9, r=2.0, divisor=1.0, i=perceptron):

    trainSet = readFile(trainFile)
    testSet = readFile(testFile)
    wVec = FeatureTrans([0]*(360+1))

    if runFunc or thresh_arr:
        if not thresh_arr:
            if divisor != 1.0:
                trainThreshold = runFunc(trainSet, divisor=divisor)
            else:
                trainThreshold = runFunc(trainSet)
        else:
            trainThreshold = thresh_arr
        preProcess(trainSet, trainThreshold)
        preProcess(testSet, trainThreshold)

        # wVec = FeatureTrans(trainThreshold.fv[:])

        if runFunc == get_threshold_one:
            wVec = FeatureTrans(trainThreshold.fv[:])

    wVec.fv[0] = 1
    avgVec = FeatureTrans([0]*(360+1))
    avgVec.fv[0] = 1
    if i == perceptron:
        for k in range(numEpoch):
            wVec, avgVec = perceptron(trainSet, wVec, avgVec, mew=mew, r=r)
            random.shuffle(trainSet)

    if average:
        correctPercent, fscore, arr = evalPerceptron(testSet, avgVec)
    else:
        correctPercent, fscore, arr = evalPerceptron(testSet, wVec)
    print('fscore: ' + str(fscore) + '\n')
    return fscore, arr
    print("percent: " + str(correctPercent) + '\n')


def outputEvalFile(wVec, testSet, evalNums, outputFile):
    out = open(outputFile, 'w')
    out.write('example_id,label\n')
    for index, example in enumerate(testSet):
        ret = wVec * example
        sign = 0 if ret < 0 else 1
        out.write(evalNums[index] + ',' + str(sign) + '\n')


def predict(trainFile, testFile, id_file, out_file, numEpoch=1,  average=False, preProcessed=None, trainThreshold=None,
                      mew=0.0, r=1.0, divisor=1.0):
    trainSet = readFile(trainFile)
    testSet = readFile(testFile)

    if preProcessed or trainThreshold:
        if not trainThreshold:
            wVec = FeatureTrans(trainThreshold)
            trainThreshold = preProcessed(trainSet, divisor=divisor)
        preProcess(trainSet, trainThreshold)
        preProcess(testSet, trainThreshold)


    wVec = FeatureTrans([0]*(360+1))

    eval_nums = read_eval_num_file(id_file)
    wVec.fv[0] = 1
    avgVec = FeatureTrans([0]*(360+1))
    avgVec.fv[0] = 1
    for i in range(numEpoch):
        wVec, avgVec = perceptron(trainSet, wVec, avgVec, mew=mew, r=r)
        random.shuffle(trainSet)
    if average:
        outputEvalFile(avgVec, testSet, eval_nums, out_file)
    else:
        outputEvalFile(wVec, testSet, eval_nums, out_file)


            

calculateOne(trainFile, testFile, numEpoch=1, average=True, thresh_arr=thresholdArrOne)


predict(trainFile, evalFile, evanNumsFile, outputFile, numEpoch=1, average=True,trainThreshold=thresholdArrOne, mew=9, r=2.0, divisor=1.0)
