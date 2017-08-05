import numpy as np
import math
from scipy.spatial import distance
import matplotlib.pyplot as plt
from util import get_data
import pandas as pd
import datetime as dt

def compute_orders_df(predY, dataFrame):
    orders_df_policy = pd.DataFrame(predY)
    prices_df = dataFrame

    #orders_df_policy['shiftedY']= (orders_df_policy['predY'].shift(1))
    #print orders_df_policy
    #signal_df = pd.DataFrame()
    #signal_df['Signal'] = (((orders_df_policy['predY'] - orders_df_policy['shiftedY']  )/orders_df_policy['shiftedY'] ) * 100)

    #signal_df['Signal'] = (((orders_df_policy['predY'] - prices_df['ML4T-220'])/prices_df['ML4T-220']) * 100)
    #print signal_df.values




    orders_df_policy['Long_entry']= ""
    orders_df_policy['Long_exit']= ""
    orders_df_policy['Short_entry']= ""
    orders_df_policy['Short_exit']= ""
    longexit = False
    shortexit= False
    orders = []
    hold = 0
    for date, column in orders_df_policy.iterrows():
        hold -= 1
        if hold < 0:
            hold = 0
        if  column['predY'] >= .01 and shortexit == False and longexit == False and hold == 0:
            orders_df_policy.ix[date,'Long_entry'] = "longentry"
            orders.append({'Date' : date, 'Symbol' : 'ML4T-220', 'Order' : "BUY", 'Shares' : 100})
            hold = 5
            longexit = True

        if  shortexit == False and longexit == True and hold == 0:
            orders_df_policy.ix[date,'Long_exit'] = "longexit"
            orders.append({'Date' : date,'Symbol' : 'ML4T-220', 'Order' : "SELL", 'Shares' : 100})
            longexit = False
            shortexit = False

        if  column['predY'] <= -.01 and shortexit == False and longexit == False and hold == 0:
            orders_df_policy.ix[date,'Short_entry'] = "shortentry"
            orders.append({'Date' : date,'Symbol' : 'ML4T-220', 'Order' : "SELL", 'Shares' : 100})
            hold = 5
            shortexit = True

        if  shortexit == True and longexit == False and hold == 0:
            orders_df_policy.ix[date,'Short_exit'] = "shortexit"
            orders.append({'Date' : date, 'Symbol' : 'ML4T-220', 'Order' : "BUY", 'Shares' : 100})
            shortexit = False
            longexit = False

    orders_df = pd.DataFrame(orders)

    long_entry = orders_df_policy[orders_df_policy['Long_entry'] == "longentry"].index.tolist()
    long_exit = orders_df_policy[orders_df_policy['Long_exit'] == "longexit"].index.tolist()
    short_entry = orders_df_policy[orders_df_policy['Short_entry'] == "shortentry"].index.tolist()
    short_exit = orders_df_policy[orders_df_policy['Short_exit'] == "shortexit"].index.tolist()

    csv_print = pd.DataFrame(orders_df, columns=['Date','Symbol','Order', 'Shares']).set_index('Date')
    csv_print.to_csv('orders1.csv',sep=",")


    return orders_df, long_entry, long_exit, short_entry, short_exit
