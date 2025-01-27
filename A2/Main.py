#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 08:59:19 2019

@author: ritesh
"""

from perceptron import Perceptron
from random import randint

import numpy as np
import matplotlib.pyplot as plt


def load_file(path, max_col_prior=0):
	store = []
	label  = []

	max_col_cnt = 0

	with open(path) as f:
		for line in f:
			data  = line.split()
			label.append(float(data[0]))
			row   = []

			col_cnt = 0
			for i, (idx, value) in enumerate([item.split(':') for item in data[1:]]):
				
				n = int(idx) - (i + 1) 


				for _ in range(n):
					row.append(0)
					col_cnt += 1 
					
				row.append(float(value))
				col_cnt += 1
			store.append(row)
			
			if(col_cnt > max_col_cnt):
				max_col_cnt = col_cnt		


	if(max_col_cnt < max_col_prior):
		max_col_cnt = max_col_prior


	for i in range(len(store)):
		for j in range(max_col_cnt - len(store[i])):
			store[i].append(0)

	return np.array(store), np.array(label), max_col_cnt


def get_accuracy(ground, predicted):
	correct = 0
	if (ground.shape[0] != predicted.shape[0]):
		print("Array sizes do not match")
		return 0.0
	
	correct = np.sum(ground == predicted)
	return float(correct)*100/ground.shape[0]

epochTr = 10
epochTe = 20
lmin = 50
lmax = 90

np.random.seed(0)

dir = 'CVfolds/'
num_folds = 5

dataCv = [] 
labelCv = []
max_col_prior = 0

    
for i in range(num_folds):
    data_fold, label_fold, max_col_prior = load_file(dir + 'fold' + str(i +1), max_col_prior)
    dataCv.append(data_fold)
    labelCv.append(label_fold)
    

dir = 'data/'
dataTr, labelTr, max_col_prior = load_file(dir + 'data_train', max_col_prior)
dataTe, labelTe, max_col_prior = load_file(dir + 'data_test', max_col_prior)


(values, counts) = np.unique(labelTr, return_counts = True)
majority_label = values[np.argmax(counts)]


prediction = np.ones(labelTr.shape)  * majority_label
print("Accuracy ML for training set = %.2f" %(get_accuracy(labelTr, prediction)))

prediction = np.ones(labelTe.shape)  * majority_label
print("Accuracy ML for test set = %.2f" %(get_accuracy(labelTe, prediction)))


def printing_func(acc_tr_list, acc_te_list, title, graphName, num_update):
    
    
    print("Total num of updates= " + str(num_update))

    acc_tr_list = np.array(acc_tr_list)

    ind = np.argmax(acc_tr_list)
    
    acc_te_list = np.array(acc_te_list)
    ind2 = np.argmax(acc_te_list)
    print('\nAccuracy on best hyperparameter\ntrain = %.2f\ntest = %.2f' %(acc_tr_list[ind], acc_te_list[ind2]))

    plt.figure()
    plt.ylim([lmin, lmax])
    plt.plot(range(1, epochTe+1), acc_tr_list, '-o')
    plt.xlabel('Epochs')
    plt.ylabel('Validation Accuracy(%)')
    plt.title(title)
    plt.grid()
    plt.savefig(graphName)
    

def crossValidation(j):
   
    if(j == 0):
        start = 1
        train_data = dataCv[1]
        train_label = labelCv[1]
        
        test_data = dataCv[0]
        test_label = labelCv[0]
    else:
        start = 0
        train_data = dataCv[0]
        train_label = labelCv[0]
        
        test_data = dataCv[j]
        test_label = labelCv[j]
        
    for k in range(start + 1, num_folds):
        if(k != j):
            train_data = np.concatenate([train_data, dataCv[k]], axis=0)
            train_label = np.concatenate([train_label, labelCv[k]], axis=0)
    
    return test_data, test_label, train_data, train_label


def decay_lr(base_lr, t):
    return float(base_lr)/(1+t)      

###########Simple Perceptron#####################
def simplePerceptron():
    lr = [1, 0.1, 0.01]
    acc = np.zeros((len(lr), num_folds))
    
    for i in range(len(lr)):
        
        for j in range(num_folds):
            
            test_data, test_label, train_data, train_label = crossValidation(j)
            
            myPerceptron = Perceptron(max_col_prior)
            myPerceptron.init_random()
            
            for k in range(epochTr):
                for l in range(train_label.shape[0]):
                    x = train_data[l]
                    y = train_label[l]
                    if(myPerceptron.predictTrain(x)*y <= 0):
                        myPerceptron.update(lr[i], x, y)
            
            test_predict = myPerceptron.predict(test_data)
            acc[i][j] = get_accuracy(test_label, test_predict)
            
            
    ###mean and std
    m = np.mean(acc, axis = 1)
    s = np.std(acc, axis = 1)
    
    print("lr \t Acc(mean) \t Acc(std)")
    for i in range(len(lr)):
        print("%.2f \t %.2f \t\t %.2f" %(lr[i], m[i], s[i]))
            
    lr_best = lr[np.argmax(m)]
    
    print("Best Learning Rate: " + str(lr_best))        
            
    myPerceptron = Perceptron(max_col_prior)
    myPerceptron.init_random()
    num_update = 0
    acc_tr_list = []
    acc_te_list = []
    
    for k in range(epochTe):
        for l in range(labelTr.shape[0]):
            x = dataTr[l]
            y = labelTr[l]
            if(myPerceptron.predictTrain(x)*y <= 0):
                myPerceptron.update(lr_best, x, y)
                num_update += 1
                
            
        predict_tr = myPerceptron.predict(dataTr)
        acc_tr = get_accuracy(labelTr, predict_tr)
        acc_tr_list.append(acc_tr)
        
        predict_te = myPerceptron.predict(dataTe)
        acc_te = get_accuracy(labelTe, predict_te)
        acc_te_list.append(acc_te)
        
    
    printing_func(acc_tr_list, acc_te_list, "Simple Perceptron", "simple.png", num_update)


 


###########Simple with decaying Perceptron###########################
def simpleWDecaying():
    lr = [1, 0.1, 0.01]
    acc = np.zeros((len(lr), num_folds))
    
    for i in range(len(lr)):
        
        for j in range(num_folds):
            
            test_data, test_label, train_data, train_label = crossValidation(j)
            
            myPerceptron = Perceptron(max_col_prior)
            myPerceptron.init_random()
            
            t = 0
            for k in range(epochTr):
                for l in range(train_label.shape[0]):
                    x = train_data[l]
                    y = train_label[l]
                    lr_t = decay_lr(lr[i], t)
                    
                    if(myPerceptron.predictTrain(x)*y <= 0):
                        myPerceptron.update(lr_t, x, y)
                        
                    t += 1
            
            test_predict = myPerceptron.predict(test_data)
            acc[i][j] = get_accuracy(test_label, test_predict)
            
            
    ###mean and std
    m = np.mean(acc, axis = 1)
    s = np.std(acc, axis = 1)
    
    print("lr \t Acc(mean) \t Acc(std)")
    for i in range(len(lr)):
        print("%.2f \t %.2f \t\t %.2f" %(lr[i], m[i], s[i]))
            
    lr_best = lr[np.argmax(m)]
    
    print("Best Learning Rata: " + str(lr_best))        
            
    myPerceptron = Perceptron(max_col_prior)
    myPerceptron.init_random()
    num_update = 0
    acc_tr_list = []
    acc_te_list = []
    
    t = 0
    for k in range(epochTe):
        for l in range(labelTr.shape[0]):
            x = dataTr[l]
            y = labelTr[l]
        
            if(myPerceptron.predictTrain(x)*y <= 0):
                myPerceptron.update(lr_best, x, y)
                num_update += 1
            
            t += 1
                
            
        predict_tr = myPerceptron.predict(dataTr)
        acc_tr = get_accuracy(labelTr, predict_tr)
        acc_tr_list.append(acc_tr)
        
        predict_te = myPerceptron.predict(dataTe)
        acc_te = get_accuracy(labelTe, predict_te)
        acc_te_list.append(acc_te)
        
    
    printing_func(acc_tr_list, acc_te_list, "Simple Perceptron(Decaying Learning Rate", "sDecay.png", num_update)
    
    
         
            
    ###############Averaged Perceptron################
    
def avgPerceptron(): 
    lr = [1, 0.1, 0.01]
    acc = np.zeros((len(lr), num_folds))
    
    for i in range(len(lr)):
        
        for j in range(num_folds):
            
            test_data, test_label, train_data, train_label = crossValidation(j)
            
            myPerceptron = Perceptron(max_col_prior, avg_flag = True)
            myPerceptron.init_random()
            
            t = 0
            for k in range(epochTr):
                for l in range(train_label.shape[0]):
                    x = train_data[l]
                    y = train_label[l]
                    
                    if(myPerceptron.predictTrain(x)*y <= 0):
                        myPerceptron.update(lr[i], x, y)
                        
                    myPerceptron.updateAvg()
            
            test_predict = myPerceptron.predict(test_data)
            acc[i][j] = get_accuracy(test_label, test_predict)
            
            
    ###mean and std
    m = np.mean(acc, axis = 1)
    s = np.std(acc, axis = 1)
    
    print("mu \t Acc(mean) \t Acc(std)")
    for i in range(len(lr)):
        print("%.2f \t %.2f \t\t %.2f" %(lr[i], m[i], s[i]))
    
    ind = np.argwhere(m == np.max(m))
    lr_best = lr[ind[0,0]]
    
    print("Best Learning Rata: " + str(lr_best))        
            
    myPerceptron = Perceptron(max_col_prior, avg_flag = True)
    myPerceptron.init_random()
    num_update = 0
    acc_tr_list = []
    acc_te_list = []
    
    t = 0
    for k in range(epochTe):
        for l in range(labelTr.shape[0]):
            x = dataTr[l]
            y = labelTr[l]
            lr_t = lr_best
            
            if(myPerceptron.predictTrain(x)*y <= 0):
                myPerceptron.update(lr_t, x, y)
                num_update += 1
            
            myPerceptron.updateAvg()
                
            
        predict_tr = myPerceptron.predict(dataTr)
        acc_tr = get_accuracy(labelTr, predict_tr)
        acc_tr_list.append(acc_tr)
        
        predict_te = myPerceptron.predict(dataTe)
        acc_te = get_accuracy(labelTe, predict_te)
        acc_te_list.append(acc_te)
        
    printing_func(acc_tr_list, acc_te_list, "Averaged Perceptron", "avg.png", num_update)
    
    
    


##################Pocket Perceptron################
def pocketPerceptron():
    lr = [1, 0.1, 0.01]
    acc = np.zeros((len(lr), num_folds))
    
    for i in range(len(lr)):
        
        for j in range(num_folds):
            
            test_data, test_label, train_data, train_label = crossValidation(j)
            
            myPerceptron = Perceptron(max_col_prior, pocket_flag = True)
            myPerceptron.init_random()
            
            t = 0
            
            for k in range(epochTr):
                first = True
                for l in range(train_label.shape[0]):
                    x = train_data[l]
                    y = train_label[l]
                    
                    
                    if(myPerceptron.predictTrain(x)*y <= 0):
                        if(first == True):
                            myPerceptron.pocket_counter = myPerceptron.current_counter
                            first = False
                        elif(myPerceptron.current_counter > myPerceptron.pocket_counter):
                            myPerceptron.wp = myPerceptron.w
                            myPerceptron.pocket_counter = myPerceptron.current_counter
                            
                        
                        myPerceptron.update(lr[i], x, y)
                        
                        myPerceptron.current_counter = 0
                    else:    
                        myPerceptron.current_counter += 1
                    
                    
            
            test_predict = myPerceptron.predict(test_data)
            acc[i][j] = get_accuracy(test_label, test_predict)
            
            
    ###mean and std
    m = np.mean(acc, axis = 1)
    s = np.std(acc, axis = 1)
    
    print("mu \t Acc(mean) \t Acc(std)")
    for i in range(len(lr)):
        print("%.2f \t %.2f \t\t %.2f" %(lr[i], m[i], s[i]))
    
    lr_best = lr[np.argmax(m)]
    
    print("Best Learning Rata: " + str(lr_best))        
            
    myPerceptron = Perceptron(max_col_prior, pocket_flag = True)
    myPerceptron.init_random()
    num_update = 0
    acc_tr_list = []
    acc_te_list = []
    
    t = 0
    
    for k in range(epochTe):
        first = True
        for l in range(labelTr.shape[0]):
            x = dataTr[l]
            y = labelTr[l]
            lr_t = lr_best
            
            if(myPerceptron.predictTrain(x)*y <= 0):
                if(first == True):
                    myPerceptron.pocket_counter = myPerceptron.current_counter
                    first = False
                elif(myPerceptron.current_counter > myPerceptron.pocket_counter):
                    myPerceptron.wp = myPerceptron.w
                    myPerceptron.pocket_counter = myPerceptron.current_counter
                
                myPerceptron.update(lr_t, x, y)
                num_update += 1
                myPerceptron.current_counter = 0
                        
            else:
                myPerceptron.current_counter += 1
                    
                
            
        predict_tr = myPerceptron.predict(dataTr)
        acc_tr = get_accuracy(labelTr, predict_tr)
        acc_tr_list.append(acc_tr)
        
        predict_te = myPerceptron.predict(dataTe)
        acc_te = get_accuracy(labelTe, predict_te)
        acc_te_list.append(acc_te)
        
        
    printing_func(acc_tr_list, acc_te_list, "Pocket Perceptron", "pocket.png", num_update)
    

print("\t\tSimple Perceptron")
simplePerceptron()
print("\n\n")
print("\t\tSimple with Decaying")
simpleWDecaying()
print("\n\n")
print("\t\tAverage Perceptron")
avgPerceptron()
print("\n\n")
print("\t\tPocket Perceptron")
pocketPerceptron()


        
    
    
    
