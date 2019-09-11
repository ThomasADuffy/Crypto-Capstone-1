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
    scatter_matrix_temp=scatter_matrix(df,figsize = (15,12))
    plt.suptitle(title,weight='bold',fontsize = 20)
    for ax in scatter_matrix_temp.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 14,weight='600', rotation = -10,y=-100)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 14,weight='600', rotation =90,x=-100)
    plt.savefig(savefig)
    plt.show()