#! /usr/bin/python
import numpy as np
import xgboost as xgb
from matplotlib import pyplot as plt
from sklearn.metrics import roc_curve


def print_stats(ypre, ytest):
    # Get Score:
    score = len(filter(lambda x:x[0] == x[1], zip(ypre,ytest)))
    nsCorrect = filter(lambda x:x[0] == x[1] and x[0] == 1 , zip(ypre,ytest))
    nsPred = filter(lambda x: x==1, ypre)
    nsActual = filter(lambda x: x==1, ytest)
#     print 'Number of actual No-Shows: %s' %len(nsActual)
    print 'Accuracy: %s' % (score*1.0/len(ytest))
    print('PPV: %s'%(len(nsCorrect)*1.0/len(nsPred))) # TP / (TP+FP)
    print 'Sensitivity or TPR : %s' % (len(nsCorrect)*1.0/(len(nsActual))) #TP / P
    
def plotRoc(ytest, scores):
    fpr, tpr, thresholds = roc_curve(ytest, scores)
    print('FPR: %s' % fpr)
    print('TPR: %s' % tpr)
    print('Thresholds: %s' % thresholds)
    print(len(thresholds))
    plt.figure(0)
    random,= plt.plot(np.arange(0,1,0.001),np.arange(0,1,0.001), label="Random")
    plt.title('ROC')
    model, = plt.plot(fpr,tpr, label="Model")
    plt.legend(handles=[model,random],loc=4)
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.figure(1)
    plt.title('Metrics V.S. Threshold ')
    tpr_plot, = plt.plot(thresholds, tpr, label='TPR')
    fpr_plot, = plt.plot(thresholds, fpr, label='FPR')
    bin_pred = pred[:]
    th = np.arange(0.05,1,0.01)
    bin_pred = [[0 if bin_pred[i]<= t else 1 for i in xrange(len(bin_pred))] for t in th]
    acc = [sum( [preds[i] == ytest[i] for i in xrange(len(ytest))] )*1.0 / float(len(ytest)) for preds in bin_pred]
    acc_plot, = plt.plot(th, acc, label='Accuracy')
    plt.legend(handles=[tpr_plot, fpr_plot, acc_plot],loc=5)
    plt.ylabel("Percentage")
    plt.xlabel("Thresholds")

# label need to be 0 to num_class -1
#xtrain = np.loadtxt('xtrain.txt', delimiter=',')
#ytrain = np.loadtxt("ytrain.txt", delimiter=" ")
#
#xtest = np.loadtxt('xtest.txt', delimiter=',')
#ytest = np.loadtxt("ytest.txt", delimiter=" ")
##
#xg_train = xgb.DMatrix(xtrain, label=ytrain)
#xg_test = xgb.DMatrix(xtest, label=ytest)
##
### setup parameters for xgboost
#param = {}
#### use softmax multi-class classification
#param['objective'] = 'binary:logistic'
### scale weight of positive examples
#param['eta'] = 0.1
#param['max_depth'] = 10
#param['silent'] = 1
#param['nthread'] = 4
#param['eval_metric'] ='auc'
#param['scale_pos_weight'] = 47747*1.0/7836
##
###
#watchlist = [ (xg_train,'train'), (xg_test, 'test') ]
#num_round = 50
#bst = xgb.train(param, xg_train, num_round, watchlist);
#

### get prediction
pred = bst.predict( xg_test );
plotRoc(ytest, pred)
#bin_pred = pred[:]
#for i in range(len(bin_pred)):
#    bin_pred[i] = 0 if bin_pred[i]<=0.65 else 1

#print ('predicting, classification error=%f' % (sum( int(pred[i]) != ytest[i] for i in range(len(ytest))) / float(len(ytest)) ))
    
#print_stats(bin_pred,ytest)
