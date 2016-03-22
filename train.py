# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 14:30:23 2016

@author: zhouyunke
"""

from sklearn import svm
import numpy as np

xtrain = np.loadtxt("xtrain3.txt", delimiter=",")
ytrain = np.loadtxt("ytrain3.txt", delimiter=" ")
xtrain2 = np.loadtxt("xtrain2.txt", delimiter=",")
ytrain2 = np.loadtxt("ytrain2.txt", delimiter=" ")

xtmp = xtrain[:10000]
ytmp = ytrain[:10000]

xtest = xtrain[75000:]
ytest = ytrain[75000:]

clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(xtmp,ytmp)

ypre = clf.predict(xtest)
score = 0
for i in range(len(ytest)):
    if ytest[i] == ypre[i]:
        score +=1
    
print score*1.0/len(ytest)



#ypre2 = clf.predict(xtest2)
#score = 0
#for i in range(len(ytest2)):
#    if ytest2[i] == ypre2[i]:
#        score +=1
#    
#print score*1.0/len(ytest2)
    