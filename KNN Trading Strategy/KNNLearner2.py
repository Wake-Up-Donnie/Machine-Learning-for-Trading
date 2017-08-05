import numpy as np
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt

class KNNLearner(object):

    def __init__(self, k=3, verbose = False):
        self.k = k
        self.datax = None
        self.datay = None

    def addEvidence(self,dataX,dataY):
        """
        @summary: Add training data to learner
        @param dataX: X values of data to add
        @param dataY: the Y training values
        """
        self.datax = dataX
        self.datay = dataY


    def meanForK(self,neigh, points):
        rowLen, coll = points.shape
        k_neighbores = np.zeros([rowLen])

        for j in range(rowLen):
                k_neighbores[j] = np.mean(self.datay[neigh[j]])
        return k_neighbores
    def query(self,points):
        """
        @summary: Estimate a set of test points given the model we built.
        @param points: should be a numpy array with each row corresponding to a specific query.
        @returns the estimated values according to the saved model.
        """
        euclidean_distance = distance.cdist(self.datax, points, 'euclidean')

        sortdist = euclidean_distance.argsort(axis=0)
        #sortdist= sortdist.tolist()
        nNeighbors = sortdist[:self.k]
        neighbors = nNeighbors.T

        result = self.meanForK(neighbors, points)

        return result


if __name__=="__main__":
    print "the secret clue is 'zzyzx'"