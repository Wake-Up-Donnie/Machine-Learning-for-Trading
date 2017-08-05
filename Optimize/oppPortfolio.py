"""Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as co
from util import get_data, plot_data

def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ['GOOG','AAPL','GLD','XOM'], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # Normalize prices
    normed = prices/prices.ix[0]
    normed_SPY = prices_SPY/prices_SPY.ix[0]
    # Allocs
    alloced =  normed * allocs

    # posVals
    pos_vals = alloced * sv
    #daily portfolio value
    port_val = pos_vals.sum(axis=1)
    # Daily returns
    daily_returns = (port_val/port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]

    #Cum returns
    cr = (port_val[-1]/port_val[0]) - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()

    # Sharpe Ratio
    sr = np.sqrt(252) * ((adr - 0) / sddr)

    # Ending value of portfolio
    ev = port_val.ix[-1,1]

    # Normalized daily portfolio
    normed_daily_portfolio = port_val/port_val.ix[0]

    # Get daily portfolio value
    #port_val = prices_SPY # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([normed_daily_portfolio, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Daily portfolio value and SPY", ylabel="Normalized price")
        plt.show()
        pass

    return cr, adr, sddr, sr, normed_daily_portfolio

def negative_sharpe(noa, prices):

    # Normalize prices
    normed = prices/prices.ix[0]
    alloced = normed * noa
    sv = 1000000
    pos_vals = alloced * sv
    #daily portfolio value
    port_val = pos_vals.sum(axis=1)
    # Daily returns
    daily_returns = (port_val/port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]

    adr = daily_returns.mean()
    sddr = daily_returns.std()

    # Sharpe Ratio
    sr = (np.sqrt(252) * ((adr - 0) / sddr) * -1)
    return np.array(sr)


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    normed_SPY = prices_SPY/prices_SPY.ix[0]
    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    noa = len(syms)
    noa = (noa * [1. / noa,])

    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bnds = tuple((0,1) for x in range(len(syms)))
    min = co.minimize(negative_sharpe, noa, args=(prices,), method='SLSQP', bounds=bnds, constraints=cons)
    allocs = np.asarray(min.x)

    cr, adr, sddr, sr, normed_daily_portfolio = assess_portfolio(sd,ed,syms, allocs.tolist())

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        df_temp = pd.concat([normed_daily_portfolio, normed_SPY], keys=['Portfolio', 'SPY'], axis=1)
        plot_data(df_temp, title="Daily Portfolio Value and SPY", ylabel="Price")
        plt.show()
        pass

    return allocs, cr, adr, sddr, sr

if __name__ == "__main__":

    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2009,1,1)
    symbols= ['GOOG','AAPL','GLD','XOM']

    allocs, cr, adr, sddr, sr = \
    optimize_portfolio(sd=dt.datetime(2009,1,1), ed=dt.datetime(2010,12,31), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=True)

    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocs
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr