# **Crypto-Captstone-1** <!-- omit in toc -->
### A study of the correlation between cryptocurrency tweets and price<!-- omit in toc -->  
![Title pic][title_pic]

[title_pic]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/imgs/Title-image.jpg
<!-- toc -->
# **Table of Contents** <!-- omit in toc -->
- [**Introduction**](#introduction)
- [**What's the data?**](#whats-the-data)
- [**Initial Questions and Assumptions**](#initial-questions-and-assumptions)
- [**Photo and Data Credits/Sources**](#photo-and-data-creditssources)


# **Introduction**
Cryptocurrency is currently a phenomenon that has taken social media and wall street by storm. It
came from being an unknown digital token based off of an ingenious math equation to becoming a way
for the average person to make millions of dollars without even knowing the functionality of it. The
purpose of this capstone is finding out the reason on why this wealth and dramatic increase of price
happened in the cryptocurrency market by analyzing relevant data. First we must look at the what creates
the value of a currency; normally the value of a currency is relative to the health of the country/s which it
comes from or used(i.e the USD($) value is based of the economic health of the U.S.A). For
cryptocurrency though the value can not be based off of a country due to its decentralized nature, so
therefor what makes this value? Though I do believe there is inherent value in cryptocurrency, my
hypothesis is the value has been socially constructed and does not represent its true value.


# **What's the data?**
In the data I have collected I will be looking for a correlation between social media(focusing on twitter data)
mentions/metrics and the price/volume of two cryptocurrencies. I will be focusing on Bitcoin and
Ethereum as those are the two coins I have collected sufficient data for proper analysis.
I'm using two Datasets. One data set contained raw json file data for all of the prices of all cryptocurrencies but in order to work with my twitter data set, I will only be using the Ethereum and Bitcion json files for financial data. The twitter dataset is actually very clean so minor manipulations were needed to get a dataframe representing truely what I wanted. The main issue I ran into was the twitter data for Bitcoin was very non consistant and had many drops by date as shown by the graph below showing the tweet counts by day vs price:  
![Messy BTC twitter data][og_btc_count_bar]

[og_btc_count_bar]https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/oldBTC_price_vs_tweets_linegraph_bar.png  

Therefor I had to find another dataset for tweets for bitcoin which I ended up utilzing. (Please reference sources at bottom).


The data had a very diffrent date range between the two coins. For Ethereum the best date range I could find was from 08/07/2015 - 02/09/2018 for both data sets. With Bitcion the tweets only went as far back as 08/01/2017 - 2018-02-09.
    ETHtweets.date_filter('2015-08-07','2018-02-09')
    BTCtweets.date_filter('2017-10-08','2018-02-09')

# **Initial Questions and Assumptions**
Before even doing cleaning I started out with some base line questions and assumptions. One of the biggest assumptions which shaped my EDA was about publicity and marketing. I've bet you've heard "All publicity is good publicity, as long as they spell your name right." or "Any publicity is good publicity". I belive this is very true in todays age especially due to the exponentially lowering constraints to move informatin around due to technological improvements. In the case of a new market like cryptocurrency I beleive this was ever so present so I approached my data with the following questions.

>How many pre-boom and post

# **Photo and Data Credits/Sources**
Title picture: https://www.reviewgeek.com/3603/best-bitcoin-and-cryptocurrency-price-tracking-apps/ 

 Pathak, Ajeet Ram (2019), “Social media data #bitcoin #Ethereum # facebook ”, Mendeley Data, v1 http://dx.doi.org/10.17632/chx9mdyydb.1 

Badiola, Jaime (2019), "Bitcoin 17.7 million Tweets and price", Kaggle Data, v2 https://www.kaggle.com/jaimebadiola/bitcoin-tweets-and-price/metadata

 Wilden, Chase (2017),"Cryptocurrency Price by Day/Hr (2013 - 2018) (w/Bitcoin)" , Data.World, Version: Updated as of 2019-07-31 https://data.world/chasewillden/cryptocurrency-price-by-date-2013-february-2018 