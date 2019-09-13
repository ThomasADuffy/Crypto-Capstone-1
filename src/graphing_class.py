from parsing_class import *
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from numpy.polynomial.polynomial import polyfit

def tweet_matrix_df(df):

    '''This creates the dataframe with 
    just tweet metrics grouped by date'''

    tweet_metrics = df.groupby('datetime')['retweets','replies','favorites']\
        .sum().reset_index().reset_index(drop=True)
    tweet_metrics.rename(columns={'datetime':'time'}, inplace=True)


    return tweet_metrics

def merge_df_on_time(df1,df2):

    ''' This function merges two df's on the column time'''

    return pd.merge(df1,df2, on='time',how='left').dropna()
   

def get_count_df():

    ''' This function outputs objects which contain the
    dataframes with the counts of tweets
    by day, twitter metrics totals associated, and the 
    btc financial data for the dates which inculde both sets of data.
    it does this by merging those three dataframes together after creating
    them.'''
    
    btc=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/Json/bitcoin.json")
    btc_copy = coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/Json/bitcoin.json")
    eth=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/Json/ethereum.json")
    ETHtweets =  crypto_csv_tweets(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/ETH-tweets/ETHtweets.csv")
    BTColdtweets = crypto_csv_tweets(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/BTC-tweets/BTC.csv")
    BTCnewtweets = crypto_csv_tweets(f"/media/{getpass.getuser()}/data/Crypto-Capstone-1/data/df_Final.csv")
    btc_copy.date_filter('2017-08-01','2018-02-09')
    btc.date_filter('2017-10-08','2018-02-09')
    eth.date_filter('2015-08-07','2018-02-09')
    ETHtweets.date_filter('2015-08-07','2018-02-09')
    BTColdtweets.date_filter('2017-10-08','2018-02-09')
    BTCold_tweet_metrics = tweet_matrix_df(BTColdtweets.data)
    ETH_tweet_metrics = tweet_matrix_df(ETHtweets.data)
    BTCold_tweet_df_count = BTColdtweets.count_tweets_by_day()
    ETH_tweet_df_count = ETHtweets.count_tweets_by_day()
    BTCnew_tweet_df_count = BTCnewtweets.count_tweets_by_day()
    BTCnew_graph_DF = merge_df_on_time(btc_copy.data, BTCnew_tweet_df_count)
    ETH_graph_DF = merge_df_on_time(merge_df_on_time(eth.data,ETH_tweet_df_count),ETH_tweet_metrics)
    BTCold_graph_DF = merge_df_on_time(merge_df_on_time(btc.data,BTCold_tweet_df_count),BTCold_tweet_metrics)
    BTCold_graph_DF.rename(columns={'market_cap_by_available_supply_value':'market_cap'}, inplace=True)
    ETH_graph_DF.rename(columns={'market_cap_by_available_supply_value':'market_cap'}, inplace=True)
    return Graphingclass(ETH_graph_DF),Graphingclass(BTCold_graph_DF),Graphingclass(BTCnew_graph_DF)


class Graphingclass(object):

    ''' This class is used to graph functions from the dataframes'''

    def __init__(self,df):
        self.data = df

    def avg_tweet_interaction(self):

        ''' This creates an avg tweet interaction
        metric which allows me to diagnose if interaction is going up
        by time'''
        self.data['avg_tweet_interaction'] = (self.data['count'])/(self.data[['retweets','replies','favorites']]\
            .sum(axis = 1, skipna = True))

    def scatter_plot(self,xcolname,ycolname,color,title,xlabel,ylabel,corr,savefig):

        x=int(max(self.data[xcolname]))/2
        y=int(min(self.data[ycolname]))-(int(min(self.data[ycolname]))/8)

        plt.figure(figsize=(15,10))

        plt.scatter(self.data[xcolname],self.data[ycolname], c=color, alpha=0.3)

        plt.title(title,fontsize = 18,weight='600')
        plt.xlabel(xlabel,fontsize = 16,weight='600')
        plt.ylabel(ylabel,fontsize = 16,weight='600')
        plt.text(x, y, f'Correlation:{corr}',ha='center', fontsize=14
                ,weight='bold',c='red')

        b, m = polyfit(self.data[xcolname], self.data[ycolname], 1)
        plt.plot(self.data[xcolname], b + m * self.data[xcolname], '-')

        plt.savefig(savefig)
        plt.show()

    def pandas_scatter_matrix(self,title,savefig=None):

        '''This plots a scatter matrix'''

        scatter_matrix_temp=scatter_matrix(self.data,figsize = (20,14))

        plt.suptitle(title,weight='bold',fontsize = 24,y=.91)

        for ax in scatter_matrix_temp.ravel():

            ax.set_xlabel(ax.get_xlabel(), fontsize = 15,weight='600'
                            , rotation = -10,labelpad=10)
            ax.set_ylabel(ax.get_ylabel(), fontsize = 15,weight='600'
                            , rotation = 55,labelpad=50)
            ax.tick_params(axis='both',labelsize=13)

        plt.savefig(savefig)
        plt.show()

    def tweet_vs_price_graph(self,title,savefig,datefilter=None,width=4):

        '''tweets vs price graph plot one figure.
        datefilter is just a list containing the startdate and enddate
        in a list like [startdate,endate]'''

        if datefilter:

            df=self.data[
                (self.data['time'] > datetime.date(datetime.strptime(datefilter[0]
                , "%Y-%m-%d")))
            & (self.data['time'] < datetime.date(datetime.strptime(datefilter[1]
                , "%Y-%m-%d")))
                        ]

        else:

            df=self.data

        min_time = min(df['time']).strftime('%m/%d/%Y')
        max_time = max(df['time']).strftime('%m/%d/%Y')

        fig, ax1 = plt.subplots(figsize=(15,12))

        color1 = 'dodgerblue'

        ax1.set_xlabel('Time',fontsize = 16,weight='600')
        ax1.bar(df['time'], df['count'], color=color1, 
                label=f'# of Tweets for {title}',align='center',width=width)
        ax1.tick_params(axis='y',labelsize=14,color=color1)
        ax1.tick_params(axis='x',labelsize=14)
        ax1.set_ylabel('Count of Tweets', color=color1,fontsize = 16,weight='600')



        ax2 = ax1.twinx() 

        color2='green'

        ax2.plot(df['time'], df['price_usd_value'], color=color2
                , label=f'Price of {title}')
        ax2.tick_params(axis='y',labelsize=14,color=color1)
        ax2.set_ylabel('Price', color=color2,fontsize = 16,weight='600')

        fig.legend(loc='upper right',fontsize = 14)
        fig.suptitle((f'From {min_time} to {max_time} '+title
                    +' Tweet Counts vs Price'), fontsize=16,weight='bold')

        plt.savefig(savefig)
        plt.show()

    def tweet_metrics_graph(self,title,savefig,datefilter=None):

        '''All the twitter metrics graph plot one figure.
        datefilter is just a list containing the startdate and enddate
        in a list like [startdate,endate]'''

        if datefilter:

            df = self.data[
                (self.data['time'] > datetime.date(datetime.strptime(datefilter[0]
                , "%Y-%m-%d")))
            & (self.data['time'] < datetime.date(datetime.strptime(datefilter[1]
                , "%Y-%m-%d")))
                            ]

        else:

            df = self.data
        
        min_time = min(df['time']).strftime('%m/%d/%Y')
        max_time = max(df['time']).strftime('%m/%d/%Y')

        fig, ax1 = plt.subplots(figsize=(20,12))

        color1 = 'green'
        ax1.set_xlabel('Time',fontsize = 18,weight='600',labelpad=5)
        ax1.plot(df['time'], df['retweets'], color=color1
                , label=f'Retweets of {title}',linewidth=3.0,alpha=.5)
        ax1.tick_params(axis='both',labelsize=14)
        ax1.set_ylabel('Number of Tweets,Replies,Favorites, and Retweets'
                        ,fontsize = 18,weight='600',labelpad=5)

        ax2 = ax1.twinx()

        ax3 = ax1.twinx() 

        ax4 = ax1.twinx() 

        color2='dodgerblue'

        ax2.plot(df['time'], df['count'], color=color2
                , label=f'# of Tweets for {title}',linewidth=3.0,alpha=.5)
        ax2.tick_params(axis='y', which='both', length=0, labelsize=0)

        color3='purple'

        ax3.plot(df['time'], df['replies'], color=color3
                , label=f'Replies for {title}',linewidth=3.0,alpha=.5)
        ax3.tick_params(axis='y', which='both', length=0, labelsize=0)

        color4='pink'
        ax4.plot(df['time'], df['favorites'], color=color4, 
        label=f'Favorites for {title}',linewidth=3.0,alpha=.5,marker='+')
        ax4.tick_params(axis='y', which='both', length=0, labelsize=0)

        fig.legend(loc='upper right',fontsize = 14)
        fig.suptitle((f'From {min_time} to {max_time} '+title+' Twitter Metrics')
                    , weight='bold',fontsize = 24,y=.91)

        plt.savefig(savefig)
        plt.show()

    def two_metrics_graph(self,dfname,col1,col2,savefig,datefilter=None):

        '''Any two metrics on one graph plot one figure.
        datefilter is just a list containing the startdate and enddate
        in a list like [startdate,endate]'''

        if datefilter:

            df=self.data[
                (self.data['time'] > datetime.date(datetime.strptime(datefilter[0]
                , "%Y-%m-%d")))
            & (self.data['time'] < datetime.date(datetime.strptime(datefilter[1]
                , "%Y-%m-%d")))
                        ]

        else:

            df=self.data

        min_time = min(df['time']).strftime('%m/%d/%Y')
        max_time = max(df['time']).strftime('%m/%d/%Y')

        fig, ax1 = plt.subplots(figsize=(16,11))

        ax1.set_xlabel('Time',fontsize = 18,weight='600',labelpad=5)

        color1 = 'green'

        ax1.plot(df['time'], df[col1], color=color1, 
                label=f'{col1.capitalize()} of {dfname}')
        ax1.tick_params(axis='y',labelsize=14,color=color1)
        ax1.tick_params(axis='x',labelsize=14)
        ax1.set_ylabel(f'{col1.capitalize()}', color=color1,fontsize = 18
                        ,weight='600')

        ax2 = ax1.twinx() 

        color2='blue'

        ax2.plot(df['time'], df[col2], color=color2, 
                label=f'{col2.capitalize()} for {dfname}')
        ax2.tick_params(axis='y',labelsize=14,color=color2)
        ax2.set_ylabel(f'{col2.capitalize()}', 
                        color=color2,fontsize = 18,weight='600')

        fig.legend(loc='upper right',fontsize = 14)
        fig.suptitle((f'From {min_time} to {max_time} '+ dfname +
                    f' {col1.capitalize()} vs {col2.capitalize()}'),
        fontsize=20,weight='bold',y=.91)

        plt.savefig(savefig)
        plt.show()

if __name__ == "__main__":
    pass