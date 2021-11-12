import datetime as dt
import pandas as pd
from pandas_datareader import data as web

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
