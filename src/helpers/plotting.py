import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

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
