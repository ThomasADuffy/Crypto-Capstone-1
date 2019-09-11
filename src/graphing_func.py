from parsing_class import *

def get_count_df():
    ''' This function outputs two dataframes with the counts merged with the 
    btc graph for the dates which inculde both sets of data'''
    
    btc=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/bitcoin.json")
    eth=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/ethereum.json")
    ETHtweets =  crypto_csv_tweets(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/ETH-tweets/ETHtweets.csv")
    BTCtweets = crypto_csv_tweets(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/BTC-tweets/BTC.csv")
    btc.date_filter('2017-10-08','2018-02-09')
    eth.date_filter('2015-08-07','2018-02-09')
    ETHtweets.date_filter('2015-08-07','2018-02-09')
    BTCtweets.date_filter('2017-10-08','2018-02-09')
    BTC_tweet_df_count = BTCtweets.count_tweets_by_day()
    ETH_tweet_df_count = ETHtweets.count_tweets_by_day()
    ETH_graph_DF=pd.merge(eth.data.copy(),ETH_tweet_df_count, on='time',how='left').dropna()
    BTC_graph_DF=pd.merge(btc.data.copy(),BTC_tweet_df_count, on='time',how='left').dropna()
    return ETH_graph_DF,BTC_graph_DF