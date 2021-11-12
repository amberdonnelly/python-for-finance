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

# get standard deviation for multiple stocks
def get_stock_mean_sd(stock_df, ticker):
    return stock_df[ticker].mean(), stock_df[ticker].std()

def get_mult_stock_mean_sd(stock_df):
    for stock in stock_df:
        mean, sd = get_stock_mean_sd(stock_df, stock)
        cov = sd / mean # coefficient of variation -- measure of the risk of a stock
        print("Stock: {:4} Mean: {:7.2f} Standard Deviation: {:2.2f}".format(stock, mean, sd))
        print("Coefficient of Variation: {}\n".format(cov))
