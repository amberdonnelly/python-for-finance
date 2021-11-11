# imports
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.core.indexes import multi
import mplfinance as mpf
import numpy as np
import pandas as pd

from pandas_datareader import data as web

### HELPERS

# save stock data to csv
def save_to_csv_from_yahoo(ticker, syear, smonth, sday, eyear, emonth, eday):
    start = dt.datetime(syear, smonth, sday)
    end = dt.datetime(eyear, emonth, eday)
    
    df = web.DataReader(ticker, 'yahoo', start, end)

    df.to_csv('./data/' + ticker + '.csv')

    return df

# return dataframe from csv
def get_df_from_csv(ticker):
    try:
        df = pd.read_csv('./data/' + ticker + '.csv')
    except FileNotFoundError:
        print('File doesn\'t exist')
    else:
        return df

# add daily return to dataframe
# updates ticker csv
def add_daily_return_to_df(df, ticker):
    df['daily_return'] = (df['Adj Close'] / df['Adj Close'].shift(1)) - 1
    df.to_csv('./data/' + ticker + '.csv')
    return df

# get total return over time
def get_return_defined_time(df, syear, smonth, sday, eyear, emonth, eday):
    start = f'{syear}-{smonth}-{sday}'
    end = f'{eyear}-{emonth}-{eday}'
    mask = (df['Date'] >= start) & (df['Date'] <= end)
    
    df2 = df.loc[mask]
    days = df2.shape[0]
    daily_ret = df2['daily_return'].mean()

    return(days * daily_ret)

# finance plot
# types: candle, line, ohlc, renko, pnf
def mplfinance_plot(ticker, chart_type, syear, smonth, sday, eyear, emonth, eday):
    start = f'{syear}-{smonth}-{sday}'
    end = f'{eyear}-{emonth}-{eday}'
    try:
        df = pd.read_csv('./data/' + ticker + '.csv')
    except FileNotFoundError:
        print('File doesn\'t exist')
    else:
        df.index = pd.DatetimeIndex(df['Date'])
        df_sub = df.loc[start:end]

        s = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 8})

        fig = mpf.figure(figsize=(12,8), style=s)
        # ax = fig.add_subplot(2,1,2)
        # av = fig.add_subplot(2,1,2, sharex=ax)

        fig_file = f'./plots/priceplot_{ticker}_{start}_{end}.png'
        # mpf.plot(df_sub, type=chart_type, mav=(3,5,7), ax=ax, volume=av, show_nontrading=True, savefig=fig_file) # averge of prev (3,5,7) observations
        mpf.plot(df_sub, type=chart_type, mav=(3,5,7), savefig=fig_file) # averge of prev (3,5,7) observations

# simple price plot
def price_plot(ticker, syear, smonth, sday, eyear, emonth, eday):
    start = f'{syear}-{smonth}-{sday}'
    end = f'{eyear}-{emonth}-{eday}'
    try:
        df = pd.read_csv('./data/' + ticker + '.csv')
    except FileNotFoundError:
        print('File doesn\'t exist')
    else:
        df.index = pd.DatetimeIndex(df['Date'])
        df_sub = df.loc[start:end]
        df_np = df_sub.to_numpy()
        
        # get adjusted close data from column 5
        np_adj_close = df_np[:,5]
        # get date data from column 1
        date_arr = df_np[:,1]

        fig = plt.figure(figsize=(12,8), dpi=100)
        axes = fig.add_axes([0.1,0.1,0.85,0.85])
        axes.xaxis.set_major_locator(plt.MaxNLocator(8))
        axes.grid(True, color='0.6', dashes=(5,2,1,2))
        # axes.set_facecolor('#FAEBD7')
        axes.plot(date_arr, np_adj_close, color='navy')

        fig_file = f'./plots/simplepriceplot_{ticker}_{start}_{end}.png'
        plt.savefig(fig_file)

# download multiple stocks
def download_multiple_stocks(syear, smonth, sday, eyear, emonth, eday, *tickers):
    for x in tickers:
        save_to_csv_from_yahoo(x, syear, smonth, sday, eyear, emonth, eday)

# merge multiple stocks in one df by column name
def merge_df_by_column_name(col_name, syear, smonth, sday, eyear, emonth, eday, *tickers):
    mult_df = pd.DataFrame()
    start = f'{syear}-{smonth}-{sday}'
    end = f'{eyear}-{emonth}-{eday}'
    for x in tickers:
        mult_df[x] = web.DataReader(x, 'yahoo', start, end)[col_name]
    return mult_df

# plot changing value of investment w multiple stocks
def plot_return_mult_stocks(investment, stock_df):
    mult_ret_df = (stock_df / stock_df.iloc[0] * investment)
    tickers = mult_ret_df.columns.to_numpy()

    df_np = mult_ret_df.to_numpy()

    fig = plt.figure(figsize=(12,8), dpi=100)
    axes = fig.add_axes([0.1,0.1,0.85,0.85])
    axes.grid(True, color='0.6', dashes=(5,2,1,2))
    axes.plot(df_np)
    axes.legend(tickers, loc ="upper left")

    tickers_str = '-'.join(tickers)
    fig_file =f'./plots/invest{investment}_{tickers_str}.png'
    plt.savefig(fig_file)

# get standard deviation for multiple stocks
def get_stock_mean_sd(stock_df, ticker):
    return stock_df[ticker].mean(), stock_df[ticker].std()

def get_mult_stock_mean_sd(stock_df):
    for stock in stock_df:
        mean, sd = get_stock_mean_sd(stock_df, stock)
        cov = sd / mean # coefficient of variation -- measure of the risk of a stock
        print("Stock: {:4} Mean: {:7.2f} Standard Deviation: {:2.2f}".format(stock, mean, sd))
        print("Coefficient of Variation: {}\n".format(cov))

### RUN

# analyze single stock: AMZN
save_to_csv_from_yahoo('AMZN', 2020, 1, 1, 2021, 1, 1)
AMZN_df = get_df_from_csv('AMZN')
AMZN_df = add_daily_return_to_df(AMZN_df, 'AMZN')
print(AMZN_df.head())
total_ret = get_return_defined_time(AMZN_df, 2020, 1, 1, 2021, 1, 1)
print('total return: ' + str(total_ret))
mplfinance_plot('AMZN', 'ohlc', 2020, 1, 1, 2021, 1, 1)
price_plot('AMZN', 2020, 1, 1, 2021, 1, 1)

# analyze multiple stocks
tickers = ['FB', 'AAPL', 'NFLX', 'GOOG']
download_multiple_stocks(2020, 1, 1, 2021, 1, 1, *tickers)
tickers = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']
multi_df = merge_df_by_column_name('Adj Close', 2020, 1, 1, 2021, 1, 1, *tickers)
plot_return_mult_stocks(100, multi_df)
get_mult_stock_mean_sd(multi_df)
