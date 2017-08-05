"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import LinRegLearner as lrl
import BagLearner as bl
import KNNLearner as knn
import matplotlib.pyplot as plt

if __name__=="__main__":
    inf = open('Data/ripple.csv')
    data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])
    print data
    # compute how much of the data is training and testing
    train_rows = math.floor(0.6* data.shape[0])
    test_rows = data.shape[0] - train_rows

    # separate out training and testing data
    trainX = data[:train_rows,0:-1]
    trainY = data[:train_rows,-1]
    testX = data[train_rows:,0:-1]
    testY = data[train_rows:,-1]
    print type(trainX)
    np.set_printoptions(threshold=np.inf)
    #print trainY
    #print "testy"



    # create a learner and train it
    #learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    #learner.addEvidence(trainX, trainY) # train it

    #learner = knn.KNNLearner(k = 3, verbose=False)
    #learner.addEvidence(trainX, trainY)
    #predY = learner.query(trainX)



    # evaluate in sample
    learner = bl.BagLearner(learner=knn.KNNLearner, kwargs={"k": 3}, bags=20, boost=False)
    learner.addEvidence(trainX, trainY)

    predY = learner.query(trainX) # get the predictions
    rmsei = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print "In sample results"
    print "RMSE: ", rmsei
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    # evaluate out of sample
    predY = learner.query(testX) # get the predictions
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]

    #plt.scatter(rmse,predY, color=['blue'])
    #plt.xlabel("Actual Data")
    #plt.ylabel("Predicted Data")
    #plt.show()


