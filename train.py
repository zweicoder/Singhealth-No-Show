# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:30:23 2016

@author: zhouyunke
"""

from sklearn import svm
import numpy as np

x = np.loadtxt("xtrain.txt", delimiter=",")
y = np.loadtxt("ytrain.txt", delimiter=" ")

train_size = len(x) * 0.7

xtrain = x[:train_size]
ytrain = y[:train_size]

xtest = x[train_size:]
ytest = y[train_size:]

# Train
# clf = svm.SVC(kernel='linear', C = 1.0)
clf = svm.LinearSVC(dual=False, C = 1.0)
clf.fit(xtrain,ytrain)


# Predict
ypre = clf.predict(xtest)

# Get Score
score = 0
for i in range(len(ytest)):
    if ytest[i] == ypre[i]:
        score +=1
    
print score*1.0/len(ytest)