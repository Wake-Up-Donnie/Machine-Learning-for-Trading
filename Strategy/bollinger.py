
import os
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data

def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window=window)

def compute_boll(sd, ed,\
                 syms, window=20):
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols

    IBM_df = prices.copy()
    IBM_df['sma'] = get_rolling_mean(IBM_df,window)
    sma = get_rolling_mean(prices,window)
    IBM_df['upper_band'] = sma + (2 * get_rolling_std(prices,window))
    IBM_df['lower_band'] = sma - (2 * get_rolling_std(prices,window))

    IBM_df['Long_entry']= ""
    IBM_df['Long_exit']= ""
    IBM_df['Short_entry']= ""
    IBM_df['Short_exit']= ""
    IBM_df['Previous_close'] = prices['IBM'].shift(1)
    IBM_df['Upper_band_previous'] = IBM_df['upper_band'].shift(1)
    IBM_df['Lower_band_previous'] = IBM_df['lower_band'].shift(1)
    IBM_df['Previous_sma'] = IBM_df['sma'].shift(1)
    longexit = False
    shortexit= False
    orders = []
    for date, column in IBM_df.iterrows():
        if column['Previous_close'] <= column['Lower_band_previous'] and column['IBM'] >= column['lower_band'] and \
                        shortexit == False and longexit == False:
            IBM_df.ix[date,'Long_entry'] = "longentry"
            orders.append({'Date' : date, 'Symbol' : 'IBM', 'Order' : "BUY", 'Shares' : 100})
            longexit = True

        if column['Previous_close'] <= column['Previous_sma'] and column['IBM'] >= column['sma'] and \
                        shortexit == False and longexit == True:
            IBM_df.ix[date,'Long_exit'] = "longexit"
            orders.append({'Date' : date,'Symbol' : 'IBM', 'Order' : "SELL", 'Shares' : 100})
            longexit = False
            longentry = False

        if column['Previous_close'] >= column['Upper_band_previous'] and column['IBM'] <= column['upper_band'] and \
                        shortexit == False and longexit == False:
            IBM_df.ix[date,'Short_entry'] = "shortentry"
            orders.append({'Date' : date,'Symbol' : 'IBM', 'Order' : "SELL", 'Shares' : 100})
            shortexit = True

        if column['Previous_close'] >= column['Previous_sma'] and column['IBM'] <= column['sma'] and \
                        shortexit == True and longexit == False:
            IBM_df.ix[date,'Short_exit'] = "shortexit"
            orders.append({'Date' : date, 'Symbol' : 'IBM', 'Order' : "BUY", 'Shares' : 100})
            shortexit = False
            longexit = False
    orders_df = pd.DataFrame(orders)

    long_entry = IBM_df[IBM_df['Long_entry'] == "longentry"].index.tolist()
    long_exit = IBM_df[IBM_df['Long_exit'] == "longexit"].index.tolist()
    short_entry = IBM_df[IBM_df['Short_entry'] == "shortentry"].index.tolist()

    short_exit = IBM_df[IBM_df['Short_exit'] == "shortexit"].index.tolist()
    chart = IBM_df['IBM'].plot(legend = 'True')
    IBM_df['sma'].plot(color = 'green', label = 'SMA',legend = 'True')
    IBM_df['upper_band'].plot( color = '#ADD8E6', label = 'Bollinger Bands',legend = 'True')
    IBM_df['lower_band'].plot( color = '#ADD8E6', label = '_nolegend_')

    chart.legend(loc='upper left')
    plt.vlines(x=short_entry, ymin=60, ymax=130, colors = "red")
    plt.vlines(x=short_exit, ymin=60, ymax=130, colors = "black")
    plt.vlines(x=long_entry, ymin=60, ymax=130, colors = "green")
    plt.vlines(x=long_exit, ymin=60, ymax=130, colors = "black")
    plt.show()

    csv_print = pd.DataFrame(orders_df, columns=['Date','Symbol','Order', 'Shares']).set_index('Date')
    csv_print.to_csv('orders.csv',sep=",")
    return csv_print


if __name__ == "__main__":

    sd = dt.datetime(2007,12,31)
    ed = dt.datetime(2009,12,31)
    syms = ['IBM']
    start_val = 10000

    csv = compute_boll(sd, ed, syms)

    of = "./orders.csv"
