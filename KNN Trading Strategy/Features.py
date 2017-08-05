import numpy as np
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt
from util import get_data
import pandas as pd
import datetime as dt


def get_rolling_mean(values, window):
    return pd.rolling_mean(values, window=window)

def get_rolling_std(values, window):
    return pd.rolling_std(values, window=window)

def compute_my_strategy(sd, ed,syms, window):
        dates = pd.date_range(sd, ed)
        prices_all = get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols

        IBM_df_plain = prices.copy()
        IBM_df = prices.copy()
        IBM_df['SMA'] = get_rolling_mean(IBM_df_plain,window)
        IBM_df['STDEV'] = get_rolling_std(IBM_df_plain, window)
        sma = get_rolling_mean(prices,window)
        IBM_df['upper_band'] = sma + (2 * get_rolling_std(prices,window))
        IBM_df['lower_band'] = sma - (2 * get_rolling_std(prices,window))
        IBM_df['bb_value'] = (IBM_df.ix[:,0] - IBM_df['SMA'])/(2 * IBM_df['STDEV'])
        IBM_df['Daily_Rets'] = (IBM_df.ix[:,0]/IBM_df.ix[:,0].shift(1)) - 1.0
        IBM_df['Vol'] = get_rolling_std(IBM_df['Daily_Rets'], window)
        IBM_df['Momentum'] = (IBM_df.ix[:,0]/ IBM_df.ix[:,0].shift(5)) - 1.0
        IBM_df['5_Day_Return'] = (IBM_df['ML4T-220'].shift(-5)/IBM_df['ML4T-220']) - 1.0


        return IBM_df

if __name__=="__main__":
    print "the secret clue is 'zzyzx'"