# from wsgiref.simple_server import make_server
# from pyramid.config import Configurator
# from pyramid.response import Response

from helpers.data import *
from helpers.plotting import *
from helpers.analysis import *

# import matplotlib.dates as mdates
# from pandas.core.indexes import multi
# import numpy as np

# analyze single stock: AMZN
# ticker = 'AMZN'
def analyze_single_stock(ticker):
    save_to_csv_from_yahoo(ticker, 2020, 1, 1, 2021, 1, 1)
    AMZN_df = get_df_from_csv(ticker)
    AMZN_df = add_daily_return_to_df(AMZN_df, ticker)
    print(AMZN_df.head())
    total_ret = get_return_defined_time(AMZN_df, 2020, 1, 1, 2021, 1, 1)
    print('total return: ' + str(total_ret))
    mplfinance_plot(ticker, 'ohlc', 2020, 1, 1, 2021, 1, 1)
    price_plot(ticker, 2020, 1, 1, 2021, 1, 1)

# analyze multiple stocks
# tickers = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']
def analyze_multiple_stocks(*tickers):
    download_multiple_stocks(2020, 1, 1, 2021, 1, 1, *tickers)
    multi_df = merge_df_by_column_name('Adj Close', 2020, 1, 1, 2021, 1, 1, *tickers)
    plot_return_mult_stocks(100, multi_df)
    get_mult_stock_mean_sd(multi_df)

# TESTING (WIP)

ticker = 'AMZN'
analyze_single_stock(ticker)

tickers = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']
analyze_multiple_stocks(*tickers)

# PYRAMID APP (TODO)

# def main(request):
#     return Response('Hello World!')

# if __name__ == '__main__':
#     with Configurator() as config:
#         config.add_route('main', '/')
#         config.add_view(main, route_name='main')
#         app = config.make_wsgi_app()
#     server = make_server('0.0.0.0', 6543, app)
#     server.serve_forever()
