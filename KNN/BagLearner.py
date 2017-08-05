import numpy as np
import math
from scipy.spatial import distance
import KNNLearner as knn
import matplotlib.pyplot as plt

class BagLearner(object):

    def __init__(self, learner =knn.KNNLearner,  kwargs = {'k':3}, bags =20, boost=False, verbose = False):
        self.learner = learner
        self.learnerList = []
        self.bags = bags
        for i in range(bags):
            self.learnerList.append(learner(**kwargs))


    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        self.datax = dataX
        self.datay = dataY
        self.dataxshape = dataX.shape[0]
        learnerList = self.learnerList
        for i in learnerList:
            random_bag = np.random.choice(np.arange(self.dataxshape), self.dataxshape, replace=True)
            xValues = self.datax[random_bag,:]
            yValues = self.datay[random_bag]
            i.addEvidence(xValues,yValues)

        #make sure y,X1 and X2 have the same indicieis


        
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        learnerList= []
        for i in self.learnerList:
            yi = i.query(points)
            learnerList.append(yi)
        yPred = np.mean(learnerList, axis = 0)

        return yPred


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"