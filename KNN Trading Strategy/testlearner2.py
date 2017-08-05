"""
Test a learner.  (c) 2015 Tucker Balch
"""

import numpy as np
import math
import Features as ft
import datetime as dt
import pandas as pd
import KNNLearner2 as knn
import matplotlib.pyplot as plt
import Policy as pol
import PortvalsGraphing as prtvals

if __name__=="__main__":
    #inf = open('Data/ripple.csv')
    #data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])

    #INSAMPLE
    sd = dt.datetime(2007,12,31)
    ed = dt.datetime(2009,12,31)
    syms = ['ML4T-220']
    window = 20
    dataFrame = ft.compute_my_strategy(sd,ed,syms, window)
    y_train_plot = pd.DataFrame(dataFrame)
    y_train_plot['ytrain_plot'] = ((dataFrame['5_Day_Return'] * dataFrame['ML4T-220']) + dataFrame['ML4T-220'])

    dataFrame_all = dataFrame.dropna()

    index_dates = dataFrame_all.index.tolist()
    features_dataframe = pd.concat([dataFrame_all['bb_value'],dataFrame_all['Vol'],dataFrame_all['Momentum']], axis=1)
    features_with_price_5_in_fut_dataframe = pd.concat([dataFrame_all['bb_value'],dataFrame_all['Vol'],
                                                        dataFrame_all['Momentum'], dataFrame_all['5_Day_Return']], axis=1)

    # compute how much of the data is training and testing
    features_with_price_5_in_fut_dataframe = features_with_price_5_in_fut_dataframe.as_matrix()

    #train_rows = math.floor(0.6*  features_with_price_5_in_fut_dataframe.shape[0])
    train_rows = features_with_price_5_in_fut_dataframe.shape[0]

    # separate out training and testing data
    trainX = features_with_price_5_in_fut_dataframe[:,0:-1]
    trainY = features_with_price_5_in_fut_dataframe[:,-1]

    #OUTOFSAMPLE

    #FILL WiTH OUT OF SAMPLE!!!
    sd = dt.datetime(2009,12,31)
    ed = dt.datetime(2011,12,31)
    syms = ['ML4T-220']
    window = 20
    dataFrame_test = ft.compute_my_strategy(sd,ed,syms, window)
    y_test_plot = pd.DataFrame(dataFrame_test)
    y_test_plot['ytest_plot'] = ((dataFrame_test['5_Day_Return'] * dataFrame_test['ML4T-220']) + dataFrame_test['ML4T-220'])

    dataFrame_all_test = dataFrame_test.dropna()

    index_dates_test = dataFrame_all.index.tolist()
    features_dataframe_test = pd.concat([dataFrame_all_test['bb_value'],dataFrame_all['Vol'],dataFrame_all_test['Momentum']], axis=1)
    features_with_price_5_in_fut_dataframe_test = pd.concat([dataFrame_all_test['bb_value'],dataFrame_all_test['Vol'],
                                                        dataFrame_all_test['Momentum'], dataFrame_all_test['5_Day_Return']], axis=1)

    # compute how much of the data is training and testing
    features_with_price_5_in_fut_dataframe_test = features_with_price_5_in_fut_dataframe_test.as_matrix()

    #train_rows = math.floor(0.6*  features_with_price_5_in_fut_dataframe.shape[0])
    test_rows = features_with_price_5_in_fut_dataframe_test.shape[0]

    # separate out training and testing data

    testX = features_with_price_5_in_fut_dataframe_test[:,0:-1]

    testY = features_with_price_5_in_fut_dataframe_test[:,-1]

    index_dates_test = dataFrame_all_test.index.tolist()

    index_dates_test = index_dates_test[:int(test_rows)]

    '''
    trainX = features_with_price_5_in_fut_dataframe[:train_rows,0:-1]
    trainY = features_with_price_5_in_fut_dataframe[:train_rows,-1]
    testX = features_with_price_5_in_fut_dataframe[train_rows:,0:-1]
    testY = features_with_price_5_in_fut_dataframe[train_rows:,-1]
    '''


    #np.set_printoptions(threshold=np.inf)
    #print trainY
    #print "testy"
    index_dates_training = dataFrame_all.index.tolist()

    index_dates_training = index_dates_training[:int(train_rows)]

    #trainY_df = pd.DataFrame(trainY, index =index_dates_training)
    #trainY_df = trainY_df.rename(columns = {0:'trainY'})

    # create a learner and train it
    #learner = lrl.LinRegLearner(verbose = True) # create a LinRegLearner
    #learner.addEvidence(trainX, trainY) # train it

    learner = knn.KNNLearner(k = 3, verbose=False)
    learner.addEvidence(trainX, trainY)
    predY = learner.query(trainX)

    predY_df = pd.DataFrame(predY,index =index_dates_training)
    predY_df = predY_df.rename(columns = {0:'predY'})
    predY_df['trainY'] = trainY
    orders_df, long_entry, long_exit, short_entry, short_exit = pol.compute_orders_df(predY_df, dataFrame)
    predY_df['predY'] = (predY_df['predY'] * dataFrame['ML4T-220']) + dataFrame['ML4T-220']

    #predY_df = predY_df.apply(lambda x: ((x - np.min(x)))*2 / (np.max(x) - np.min(x))-1) #CHANGE
    #print predY_df

    #print orders_df

    #predY_df['trainY'] = predY_df['trainY'] / predY_df['trainY'].ix[0]
    #predY_df['predY'] = predY_df['predY']/predY_df['predY'].ix[0]


    orig_price = dataFrame_all['ML4T-220'].as_matrix()
    orig_price_df = pd.DataFrame(orig_price, index=index_dates)
    orig_price_df = orig_price_df.rename(columns = {0:'orig_price'})
    orig_price_df['orig_price'] = orig_price_df['orig_price'] / orig_price_df['orig_price'].ix[0]
    #predY_df['predY'] = (predY_df['predY'] * dataFrame['ML4T-220']) + dataFrame['ML4T-220']
    rmsei = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
    print "In sample results"
    print "RMSE: ", rmsei
    c = np.corrcoef(predY, y=trainY)
    print "corr: ", c[0,1]

    '''
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
    '''

    plt.figure()
    ax = dataFrame['ML4T-220'].plot(color = 'blue', label = 'ML4T-220',legend = 'True')
    y_train_plot['ytrain_plot'].plot(color = 'black', label = 'trainY',legend = 'True')
    predY_df['predY'].plot(color = 'green', label = 'predY',legend = 'True')
    ax.set_xlabel("Dates")
    ax.set_ylabel("Price")
    ax.set_title("Original Price, Y pred and Y Train")
    xlims = ax.get_xlim()
    print xlims
    ax.set_xlim((733041.0, 733200.0))
    ylims = ax.get_ylim()
    print ylims
    ax.set_ylim((315, 345))
    plt.vlines(x=short_entry,ymin=80, ymax=dataFrame['ML4T-220'].max(),colors = "red")
    plt.vlines(x=short_exit, ymin=80, ymax=dataFrame['ML4T-220'].max(), colors = "black")
    plt.vlines(x=long_entry, ymin=80, ymax=dataFrame['ML4T-220'].max(), colors = "green")
    plt.vlines(x=long_exit, ymin=80, ymax=dataFrame['ML4T-220'].max(), colors = "black")

    #ax.set_xlabel('Date')
    #ax.set_ylabel('Predictions')
    #predY_df['predY'].plot(label='PredY', ax=ax, color='b')
    #predY_df['trainY'].plot(label='trainY', ax=ax, color='g')
    #orig_price_df['orig_price'].plot(label='ML4T-220', ax=ax, color='red')
    ax.legend(loc=2)
    plt.show()
    #plt.scatter(rmse,predY, color=['blue'])
    #plt.xlabel("Actual Data")
    #plt.ylabel("Predicted Data")
    #plt.show()
    of = "./orders1.csv"

    final_port_val_IBM, sr_IBM, cr_IBM, sddr_IBM, adr_IBM, adr_IBM, sr_SPX, cr_SPX, sddr_SPX, adr_SPX, start_date, \
        end_date= prtvals.compute_portvals(of, sd, ed, syms, start_val = 10000)
    print "In Sample ML4T-220"
    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Sharpe Ratio of Fund: {}".format(sr_IBM)
    print "Sharpe Ratio of SPX : {}".format(sr_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cr_IBM)
    print "Cumulative Return of SPX : {}".format(cr_SPX)
    print
    print "Standard Deviation of Fund: {}".format(sddr_IBM)
    print "Standard Deviation of SPX : {}".format(sddr_SPX)
    print
    print "Average Daily Return of Fund: {}".format(adr_IBM)
    print "Average Daily Return of SPX : {}".format(adr_SPX)
    print
    #portvals = portvals[portvals.columns[0]]
    print "Final Portfolio Value: {}".format(final_port_val_IBM)

    '''
    OUT OF SAMPLE
    '''
    predY = learner.query(testX)

    predY_df = pd.DataFrame(predY,index =index_dates_test)
    predY_df = predY_df.rename(columns = {0:'predY'})
    predY_df['testY'] = testY
    orders_df, long_entry, long_exit, short_entry, short_exit = pol.compute_orders_df(predY_df, dataFrame_test)
    predY_df['predY'] = (predY_df['predY'] * dataFrame_test['ML4T-220']) + dataFrame_test['ML4T-220']

    #predY_df = predY_df.apply(lambda x: ((x - np.min(x)))*2 / (np.max(x) - np.min(x))-1) #CHANGE
    #print predY_df

    #print orders_df

    #predY_df['trainY'] = predY_df['trainY'] / predY_df['trainY'].ix[0]
    #predY_df['predY'] = predY_df['predY']/predY_df['predY'].ix[0]


    orig_price = dataFrame_all_test['ML4T-220'].as_matrix()
    orig_price_df = pd.DataFrame(orig_price, index=index_dates_test)
    orig_price_df = orig_price_df.rename(columns = {0:'orig_price'})
    orig_price_df['orig_price'] = orig_price_df['orig_price'] / orig_price_df['orig_price'].ix[0]

    plt.figure()
    ax = dataFrame_test['ML4T-220'].plot(color = 'blue', label = 'ML4T-220 Test',legend = 'True')
    y_test_plot['ytest_plot'].plot(color = 'black', label = 'Ytest',legend = 'True')
    predY_df['predY'].plot(color = 'green', label = 'predY',legend = 'True')
    ax.set_xlabel("Dates")
    ax.set_ylabel("Price")
    ax.set_title("Original Price, Y pred and Y Test Out of Sample")
    xlims = ax.get_xlim()
    #ax.set_xlim((733772.0, 734000.0))
    print xlims
    ylims = ax.get_ylim()
    #ax.set_ylim((315.0, 345.0))
    print ylims

    plt.vlines(x=short_entry,ymin=310, ymax=dataFrame_test['ML4T-220'].max(),colors = "red")
    plt.vlines(x=short_exit, ymin=310, ymax=dataFrame_test['ML4T-220'].max(), colors = "black")
    plt.vlines(x=long_entry, ymin=310, ymax=dataFrame_test['ML4T-220'].max(), colors = "green")
    plt.vlines(x=long_exit, ymin=310, ymax=dataFrame_test['ML4T-220'].max(), colors = "black")

    #ax.set_xlabel('Date')
    #ax.set_ylabel('Predictions')
    #predY_df['predY'].plot(label='PredY', ax=ax, color='b')
    #predY_df['trainY'].plot(label='trainY', ax=ax, color='g')
    #orig_price_df['orig_price'].plot(label='ML4T-220', ax=ax, color='red')
    ax.legend(loc=2)
    plt.show()
    #plt.scatter(rmse,predY, color=['blue'])
    #plt.xlabel("Actual Data")
    #plt.ylabel("Predicted Data")
    #plt.show()
    rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])

    print "Out of sample results"
    print "RMSE: ", rmse
    c = np.corrcoef(predY, y=testY)
    print "corr: ", c[0,1]
    of2 = "./orders1.csv"

    final_port_val_IBM, sr_IBM, cr_IBM, sddr_IBM, adr_IBM, adr_IBM, sr_SPX, cr_SPX, sddr_SPX, adr_SPX, start_date, \
        end_date= prtvals.compute_portvals(of2, sd, ed, syms, start_val = 10000)
    print "Out Of Sample ML4T-220"
    print "Date Range: {} to {}".format(sd, ed)
    print
    print "Sharpe Ratio of Fund: {}".format(sr_IBM)
    print "Sharpe Ratio of SPX : {}".format(sr_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cr_IBM)
    print "Cumulative Return of SPX : {}".format(cr_SPX)
    print
    print "Standard Deviation of Fund: {}".format(sddr_IBM)
    print "Standard Deviation of SPX : {}".format(sddr_SPX)
    print
    print "Average Daily Return of Fund: {}".format(adr_IBM)
    print "Average Daily Return of SPX : {}".format(adr_SPX)
    print
    #portvals = portvals[portvals.columns[0]]
    print "Final Portfolio Value: {}".format(final_port_val_IBM)
