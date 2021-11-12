from helpers.data import *
from helpers.plotting import *
from helpers.analysis import *

# import matplotlib.dates as mdates
# from pandas.core.indexes import multi
# import numpy as np

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
