
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data


def rsi(prices, n):
    '''
    Got function from: "http://matplotlib.org/examples/pylab_examples/finance_work2.html"
    '''
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n
    down = -seed[seed < 0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n - 1) + upval)/n
        down = (down*(n - 1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi


def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)


def compute_my_strategy(sd, ed,syms):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols

    IBM_df = prices.copy()

    IBM_df['3d'] = np.round(get_rolling_mean(IBM_df['IBM'],window=3), 2)
    IBM_df['60d'] = np.round(get_rolling_mean(IBM_df['IBM'],window=60), 2)

    IBM_df['3d-60d'] = IBM_df['3d'] - IBM_df['60d']
    IBM_df['Mv'] = np.where(IBM_df['3d-60d'] > 1, 1,0)
    IBM_df['Mv'] = np.where(IBM_df['3d-60d'] < -1, -1, IBM_df['Mv'])

    IBM_df['rsi'] = rsi(IBM_df['IBM'], 2)

    IBM_df['Long_entry']= ""
    IBM_df['Long_exit']= ""
    IBM_df['Short_entry']= ""
    IBM_df['Short_exit']= ""
    IBM_df['Previous_rsi'] = IBM_df['rsi'].shift(1)
    IBM_df['Upper_band_previous'] = 70
    IBM_df['upper_band'] = 70
    IBM_df['Lower_band_previous'] = 30
    IBM_df['lower_band'] = 30
    IBM_df['sma'] = 50
    IBM_df['Previous_sma'] = 50
    longexit = False
    shortexit= False
    orders = []
    for date, column in IBM_df.iterrows():
        if  column['Mv'] == 1 and column['Previous_rsi'] <= column['Lower_band_previous'] and \
                        column['rsi'] >= column['lower_band'] and shortexit == False and longexit == False:
            IBM_df.ix[date,'Long_entry'] = "longentry"
            orders.append({'Date' : date, 'Symbol' : 'IBM', 'Order' : "BUY", 'Shares' : 100})
            longexit = True

        if column['Mv'] == 0 and column['Mv'] == 0 and column['Previous_rsi'] <= column['Previous_sma'] and \
                        column['rsi'] >= column['sma'] and shortexit == False and longexit == True:
            IBM_df.ix[date,'Long_exit'] = "longexit"
            orders.append({'Date' : date,'Symbol' : 'IBM', 'Order' : "SELL", 'Shares' : 100})
            longexit = False
            longentry = False

        if  column['Mv'] == -1 and column['Previous_rsi'] >= column['Upper_band_previous'] and \
                        column['rsi'] <= column['upper_band'] and shortexit == False and longexit == False:
            IBM_df.ix[date,'Short_entry'] = "shortentry"
            orders.append({'Date' : date,'Symbol' : 'IBM', 'Order' : "SELL", 'Shares' : 100})
            shortexit = True

        if  column['Mv'] == 0 and column['Previous_rsi'] >= column['Previous_sma'] and \
                        column['rsi'] <= column['sma'] and shortexit == True and longexit == False:
            IBM_df.ix[date,'Short_exit'] = "shortexit"
            orders.append({'Date' : date, 'Symbol' : 'IBM', 'Order' : "BUY", 'Shares' : 100})
            shortexit = False
            longexit = False

    orders_df = pd.DataFrame(orders)

    long_entry = IBM_df[IBM_df['Long_entry'] == "longentry"].index.tolist()
    long_exit = IBM_df[IBM_df['Long_exit'] == "longexit"].index.tolist()
    short_entry = IBM_df[IBM_df['Short_entry'] == "shortentry"].index.tolist()
    short_exit = IBM_df[IBM_df['Short_exit'] == "shortexit"].index.tolist()

    plt.figure(1)
    plt.subplot(211)
    IBM_df['IBM'].plot(legend = 'True')
    IBM_df['60d'].plot(color = 'black', label = '60d',legend = 'True')
    IBM_df['3d'].plot(color = '#FFA500', label = '3d',legend = 'True')
    plt.vlines(x=short_entry,ymin=60, ymax=IBM_df['IBM'].max(),colors = "red")
    plt.vlines(x=short_exit, ymin=60, ymax=IBM_df['IBM'].max(), colors = "black")
    plt.vlines(x=long_entry, ymin=60, ymax=IBM_df['IBM'].max(), colors = "green")
    plt.vlines(x=long_exit, ymin=60, ymax=IBM_df['IBM'].max(), colors = "black")

    plt.subplot(212)
    IBM_df['rsi'].plot(color = '#D2B48C', label = 'rsi',legend = 'True')
    plt.axhline(y=70,color = 'black')
    plt.axhline(y=30,color = 'black')
    plt.axhline(y=50,color = 'black')

    plt.vlines(x=short_entry, ymin=0, ymax=100, colors = "red")
    plt.vlines(x=short_exit, ymin=0, ymax=100, colors = "black")
    plt.vlines(x=long_entry, ymin=0, ymax=100, colors = "green")
    plt.vlines(x=long_exit, ymin=0, ymax=100, colors = "black")
    plt.show()


    csv_print = pd.DataFrame(orders_df, columns=['Date','Symbol','Order', 'Shares']).set_index('Date')
    csv_print.to_csv('orders.csv',sep=",")

    return csv_print


if __name__ == "__main__":

    sd = dt.datetime(2009,12,31)
    ed = dt.datetime(2011,12,31)
    syms= ['IBM']
    start_val = 10000

    csv_print = compute_my_strategy(sd, ed, syms)
    of = "./orders.csv"

