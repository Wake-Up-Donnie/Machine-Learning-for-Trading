import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import scipy.optimize as co

def symbol_to_path(symbol, base_dir=os.path.join("..", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates, addSPY=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df
def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def compute_portvals(orders_file, sd, ed, syms, start_val = 10000):
    # this is the function the autograder will call to test your code
    # TODO: Your code here
    orders_df_dates = pd.read_csv(orders_file, parse_dates=True)
    orders_df = pd.read_csv(orders_file,index_col='Date', parse_dates=True, na_values=['nan']).sort_index()
    symbols = []
    for i, row in orders_df.iterrows():
        if row['Symbol'] not in symbols:
            symbols.append(row['Symbol'])

    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    dates = pd.date_range(start_date,end_date)

    prices_all = get_data(['ML4T-220'], dates)

    prices_SPX = get_data(['$SPX'], dates)
    prices_SPX = prices_SPX.drop('SPY', axis=1)
    prices_all = prices_all.drop('SPY', axis=1)

    prices_df = prices_all.copy()
    prices_df['Cash'] = 1.0

    trades_df = prices_df.copy()
    trades_df[trades_df != 0] = 0

    for index, row in orders_df_dates.iterrows():
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

    portvals_IBM = value_df.copy()
    portvals_IBM = portvals_IBM.sum(axis=1)
    portvals_IBM_df = pd.DataFrame(portvals_IBM)

    final_port_val_IBM = portvals_IBM.ix[-1,1]
    normed_SPX = prices_SPX/prices_SPX.ix[0]
    portvals_SPX = normed_SPX.sum(axis=1)

    normed_daily_portfolio_IBM = portvals_IBM /portvals_IBM.ix[0]
    normed_daily_portfolio_IBM.name = 'Portfolio'

    daily_returns_IBM = (portvals_IBM /portvals_IBM .shift(1)) - 1
    daily_returns_IBM  = daily_returns_IBM [1:]

    #Cum returns
    cr_IBM = (portvals_IBM[-1]/portvals_IBM[0]) - 1
    adr_IBM  = daily_returns_IBM.mean()
    sddr_IBM  = daily_returns_IBM.std()

    # Sharpe Ratio
    sr_IBM = np.sqrt(252) * ((adr_IBM  - 0) / sddr_IBM)

    daily_returns_SPX = (portvals_SPX /portvals_SPX.shift(1)) - 1
    daily_returns_SPX  = daily_returns_SPX [1:]

    #Cum returns
    cr_SPX = (portvals_SPX[-1]/portvals_SPX[0]) - 1
    adr_SPX  = daily_returns_SPX.mean()
    sddr_SPX  = daily_returns_SPX.std()

    # Sharpe Ratio
    sr_SPX = np.sqrt(252) * ((adr_SPX - 0) / sddr_SPX)
    df_temp = pd.concat([normed_daily_portfolio_IBM, normed_SPX], axis=1)
    plot_data(df_temp, title="Daily portfolio value and $SPX", ylabel="Normalized price")
    plt.show()


    return final_port_val_IBM, sr_IBM, cr_IBM, sddr_IBM, adr_IBM, adr_IBM, sr_SPX, cr_SPX, sddr_SPX, adr_SPX,\
           start_date, end_date
