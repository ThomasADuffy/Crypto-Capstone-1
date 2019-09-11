from parsing_class import *
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix

def get_count_df():
    ''' This function outputs two dataframes with the counts merged with the 
    btc graph for the dates which inculde both sets of data'''

    btc=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/Json/bitcoin.json")
    eth=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/Json/ethereum.json")
    ETHtweets =  crypto_csv_tweets(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/ETH-tweets/ETHtweets.csv")
    BTCtweets = crypto_csv_tweets(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/BTC-tweets/BTC.csv")
    btc.date_filter('2017-10-08','2018-02-09')
    eth.date_filter('2015-08-07','2018-02-09')
    ETHtweets.date_filter('2015-08-07','2018-02-09')
    BTCtweets.date_filter('2017-10-08','2018-02-09')
    BTC_tweet_df_count = BTCtweets.count_tweets_by_day()
    ETH_tweet_df_count = ETHtweets.count_tweets_by_day()
    ETH_graph_DF=pd.merge(eth.data.copy(),ETH_tweet_df_count, on='time',how='left').dropna()
    BTC_graph_DF=pd.merge(btc.data.copy(),BTC_tweet_df_count, on='time',how='left').dropna()
    return ETH_graph_DF,BTC_graph_DF

def scatter_plot(df,xcolname,ycolname,color,title,xlabel,ylabel,corr,savefig):
    x=int(max(df[xcolname]))/2
    y=int(min(df[ycolname]))-(int(min(df[ycolname]))/8)
    plt.figure(figsize=(15,10))
    plt.scatter(df[xcolname],df[ycolname], c=color, alpha=0.3)
    plt.title(title,fontsize = 18,weight='600')
    plt.xlabel(xlabel,fontsize = 16,weight='600')
    plt.ylabel(ylabel,fontsize = 16,weight='600')
    plt.text(x, y, f'Correlation:{corr}',ha='center', fontsize=14,weight='bold',c='red')
    plt.savefig(savefig)
    plt.show()

def pandas_scatter_matrix(df,title,savefig=None):

    '''This plots a scatter matrix'''

    scatter_matrix_temp=scatter_matrix(df,figsize = (15,12))
    plt.suptitle(title,weight='bold',fontsize = 20)
    for ax in scatter_matrix_temp.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 14,weight='600', rotation = -10,y=-100)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 14,weight='600', rotation =90,x=-100)
    plt.savefig(savefig)
    plt.show()

def tweet_vs_price_graph(df,title,savefig,datefilter=None):
    '''tweets vs price graph plot one figure.
    datefilter is just a list containing the startdate and enddate
    in a list like [startdate,endate]'''

    if datefilter:
        df=df[
            (df['time'] > datetime.date(datetime.strptime(datefilter[0], "%Y-%m-%d")))
         & (df['time'] < datetime.date(datetime.strptime(datefilter[1], "%Y-%m-%d")))]
    
    min_time = min(df['time']).strftime('%m/%d/%Y')
    max_time = max(df['time']).strftime('%m/%d/%Y')
    fig, ax1 = plt.subplots(figsize=(15,12))

    color1 = 'green'
    ax1.set_xlabel('Time',fontsize = 16,weight='600')
    ax1.plot(df['time'], df['price_usd_value'], color=color1, label=f'Price of {title}')
    ax1.tick_params(axis='y',labelsize=14,color=color1)
    ax1.tick_params(axis='x',labelsize=14)
    ax1.set_ylabel('Price', color=color1,fontsize = 16,weight='600')



    ax2 = ax1.twinx() 
    color2='dodgerblue'
    ax2.plot(df['time'], df['count'], color=color2, label=f'# of Tweets for {title}')
    ax2.tick_params(axis='y',labelsize=14,color=color1)
    ax2.set_ylabel('Count of Tweets', color=color2,fontsize = 16,weight='600')
    fig.legend(loc='upper right',fontsize = 14)
    fig.suptitle((f'From {min_time} to {max_time} '+title+' Tweet Counts vs Price'), fontsize=16,weight='bold')
    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(savefig)
    plt.show()