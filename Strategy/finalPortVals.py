"""Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data



def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    orders_df_date = pd.read_csv(orders_file, parse_dates=True).sort_index()
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan']).sort_index()

    symbols = []
    for i, row in orders_df.iterrows():
        if row['Symbol'] not in symbols:
            symbols.append(row['Symbol'])

    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    dates = pd.date_range(start_date,end_date)

    prices_all = get_data(symbols, dates)
    prices_all = prices_all.drop('SPY', axis=1)

    prices_df = prices_all.copy()
    prices_df['Cash'] = 1.0

    trades_df = prices_df.copy()
    trades_df[trades_df != 0] = 0

    for index, row in orders_df_date.iterrows():
        symbol = row['Symbol']
        if row['Order'] == 'BUY':
            trades_df.ix[row.Date, symbol] += row['Shares'] * 1.0
            trades_df.ix[row.Date,'Cash'] += row['Shares'] * prices_all.ix[row.Date, symbol] * -1.0
        else:
            trades_df.ix[row.Date, symbol] += row['Shares'] * -1.0
            trades_df.ix[row.Date,'Cash'] += row['Shares'] * prices_all.ix[row.Date, symbol] * 1.0

    holdings_df = trades_df.copy()
    holdings_df[holdings_df != 0] = 0
    holdings_df = trades_df.cumsum()
    holdings_df['Cash'] = start_val + holdings_df['Cash']

    value_df = trades_df.copy()
    value_df[value_df != 0] = 0
    value_df = prices_df * holdings_df

    portvals = value_df.copy()
    portvals = portvals.sum(axis=1)
    portvals = pd.DataFrame(portvals)

    return  portvals

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    portvals = compute_portvals(orders_file = of, start_val = sv)
    #print portvals

    #print portvals
    #Process orders
    #portvals = compute_portvals(orders_file = of, start_val = sv)
    #if isinstance(portvals, pd.DataFrame):
        #portvals = portvals[portvals.columns[0]] # just get the first column
    #else:
        #"warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    #start_date = dt.datetime(2011,01,14)
    #end_date = dt.datetime(2011,12,14)
    #symbol = ['$SPX']
    #cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    #crS, adrS, sddrS, srS = assess_portfolio(sd = start_date ,ed =end_date,\
                                             #allocs = [1.0],syms=symbol)

    # Compare portfolio against $SPX
    #print "Date Range: {} to {}".format(start_date, end_date)
    #print
    #print "Sharpe Ratio of Fund: {}".format(sr)
    #print "Sharpe Ratio of SPY : {}".format(srS)
    #print
    #print "Cumulative Return of Fund: {}".format(cr)
    #print "Cumulative Return of SPY : {}".format(crS)
    #print
    #print "Standard Deviation of Fund: {}".format(sddr)
    #print "Standard Deviation of SPY : {}".format(sddrS)
    #print
    #print "Average Daily Return of Fund: {}".format(adr)
    #print "Average Daily Return of SPY : {}".format(adrS)
    #print
    portvals = portvals[portvals.columns[0]]
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
