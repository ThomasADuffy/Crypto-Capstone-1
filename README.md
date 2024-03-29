# **An Analysis of Social Media Infuence on Cryptocurrency** <!-- omit in toc -->
### A study of the correlation between cryptocurrency tweets and price<!-- omit in toc -->  
![Title pic][title_pic]

[title_pic]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/imgs/Title-image.jpg
# **Table of Contents** <!-- omit in toc -->
- [**Introduction**](#introduction)
- [**What's the data?**](#whats-the-data)
- [**Initial Question and Assumptions**](#initial-question-and-assumptions)
- [**EDA and Cleaning of Data**](#eda-and-cleaning-of-data)
- [**Visualization**](#visualization)
- [**Analysis and Conclusion**](#analysis-and-conclusion)
- [**Moving Forward**](#moving-forward)
- [**Photo and Data Credits/Sources**](#photo-and-data-creditssources)
  - [Picture sources](#picture-sources)
  - [Datasets sources](#datasets-sources)


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
I'm using Three Datasets. One data set contained raw json file data for all of the prices of all cryptocurrencies but in order to work with my twitter data set, I will only be using the Ethereum and Bitcion json files for financial data. The twitter dataset is actually very clean so minor manipulations were needed to get a dataframe representing truely what I wanted. One issue I ran into was the twitter data for Bitcoin from my original data set had many inconsistencies by date. Therefor I had to find another dataset for tweets for bitcoin which I ended up utilzing. I will go into this further in the [EDA Section.](#eda-and-cleaning-of-data)  
![Bitcoin](https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/imgs/BTC_Logo.png) <img src="https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/imgs/ETH_logo.png" height="256">


# **Initial Question and Assumptions**
Before doing any cleaning or EDA, I started out with some baseline questions and assumptions. One of the biggest assumptions which shaped my EDA was about publicity and marketing. I've bet you've heard "All publicity is good publicity, as long as they spell your name right." or "Any publicity is good publicity". I belive this is very true in todays age especially due to the exponentially lowering constraints to get information due to technological improvements. In the case of a new market like cryptocurrency I believe this was ever so present so I approached my data with the main question.

><span style=font-size:1.1em;>Is the correlation between the count of tweets per day and price of each coin?</span>  
> And if there is a correlation, is this a negative or positive correlation?

# **EDA and Cleaning of Data**
I utilized two Jupyter notebooks to do my EDA. Within these notebooks, I loaded in the data and looked at all the information and started to formulate how to gather the data I wanted from these respective files. I realized the best way was to create a class so as I looked into each data set I started to write class's for each respective file type.

First I dove into the Json files which contained financial data scraped from coinmarketcap. These json files contain a single dictionary with four key headers: market_cap_by_available_supply, price_btc, price_usd, and volume_usd. Each one of these keys values was a a list of two item lists. After some reasearch I found out that the the first item in each of the lists was a unix time stamp with the second item being the actual value of the key. Therefor I wrote a class that would parse through each of these keys and populate a pandas dataframe with the unix time stamp (converted to a date time object) as a column and the values as the other columns.   

The resulting class is within the parsing_class python file labeled:
```python
class coinmarketcap_jsonfile(object)
```  

I then started to go through the csv files of the twitter data. Luckly the Ethereum twitter file was only one file to begin with so creating a class to clean the data and export it into a pandas dataframe much like the json files. The Bitcoin twitter data though was split up into 12 diffrent csv files. So I created a python csv merger program which is located in the csv_combiner python file.  
The [code](https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/src/csv_combiner.py) is as follows:  
```python
def csv_combiner(csv_header,csv_out,csv_dir,csv_list):
    ''' This function combines csv files which were split up with the same headers into one
        
        Input
        ------
        csv_header - This is the actually header in plain text which is present in all of the CSV files
        csv_out - This is file name which you want to write the new combined csv file
        csv_dir - this is the folder containing all of the CSVs
        csv_list - this is a lst of all the file names to combine
        
        Return
        -------
        Technically nothing but it will write the csv in that folder designated'''


    csv_merge = open(csv_dir+csv_out, 'w')
    csv_merge.write(csv_header)
    csv_merge.write('\n')

    for file in csv_list:
        csv_in = open(csv_dir+f"{file}")
        for line in csv_in:
            if line.startswith(csv_header):
                continue
            csv_merge.write(line)
        csv_in.close()
    csv_merge.close()
    print('Please Verify consolidated CSV file : ' + csv_out)
```
After running this function on the Bitcoin twitter csv files, I ended up getting one csv file and was able to run this in the class I created to clean the data.  

The class I created for both of these twitter files is  is within the parsing_class python file:
```python
class crypto_csv_tweets(object)
```  
To view my class's please refer to the file [here.](https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/src/parsing_class.py)

After creating these class's I started to load in the data and exploring it. I noticed the bitcoin twitter csv file contained alot of inconsistancies. It seems that some most days didnt have any tweets, which was very trivial for what I was looking to accomplish.It also had a very small date range, which did not help either. Below is a graph which shows the original set of data where each bar is a day.  
![Messy BTC twitter data][og_btc_count_bar]

[og_btc_count_bar]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/oldBTC_price_vs_tweets_linegraph_bar.png  

Therefor I found another dataset which contained the counts of tweets per hour for a larger time frame and was more consistant and utilized that for my bitcoin twitter data. The dataset was from kaggle and had the count for tweets per hour which contained bitcoin. since it was a csv, I was able to utlize the class I already had which made importing and cleaning it extremely easy. All I had to do for this data set was a groupby query and sum the counts so I could get a count by day.

The datasets used also had a very diffrent date range between the two coins. The dates for the financial data of the coins spaned from the start of coinmarketcap keeping track of the coin to 02/09/2018. Therefor I didnt really have any issue with the date range. The only parameter which restricted my dates was the range of time which the twitter data covered.  For Ethereum the  date range was from 08/07/2015 - 02/09/2018 for both data sets. With Bitcion the tweets only went as far back as 08/01/2017 - 02/09/2018  so it was a much shorter time frame.  

The two EDA notebooks can be found [here.](https://github.com/ThomasADuffy/Crypto-Capstone-1/tree/master/notebooks)
# **Visualization**
After utilzing my classes with the data, I was finally able to get it into a format which was usable I liked and was able to start plotting. I created a file called graphing_class that contained functions and a class to graph plots which I thought would show a good representation of what I wanted to find. I ended up running all of my graphing out of a jupter note book in order to make it alot more seemless(you can look at the notebook [here](https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/notebooks/graphing_notebook.ipynb)). You can view the graphing python file which contains the class and functions [here.](https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/src/graphing_class.py)  

First I created Scatter matrix for both of the coins  

![ETH Scatter matrix][ETH_scatter_matrix]

[ETH_scatter_matrix]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/ETH_scatter_matrix.png  

![BTC Scatter matrix][BTC_scatter_matrix]

[BTC_scatter_matrix]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/newBTC_scatter_matrix.png  

Afterwards I saw a clear correlation between both tweets count and price so I decided to make actual scatter plots with regression lines for both also.I also created a correlation metrics between the two columns, price and count by utilzing the numpy.polynomial.polyfit module.  

![ETH Scatter plot][ETH_scatter_plot]

[ETH_scatter_plot]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/ETH_scatter_plot.png

![BTC Scatter plot][BTC_scatter_plot]

[BTC_scatter_plot]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/newBTC_scatter_plot.png  

In order to see if I could get a better view of the correlation, I ploted the count vs the price on a same graph which gave me these results.  

![ETH line bar][ETH_line_bar]

[ETH_line_bar]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/ETH_price_vs_tweets_linegraph.png  

![BTC line bar][BTC_line_bar]

[BTC_line_bar]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/newBTC_price_vs_tweets_linegraph_bar.png  

I created alot more graphs which you can look at [here.](https://github.com/ThomasADuffy/Crypto-Capstone-1/tree/master/graphs). This includes graphs I created with the bad set of Bitcoin data and also more graphs surrounding the Ethereum twitter metrics.
# **Analysis and Conclusion**
From the scatter matrix's you can see a clear correlation between count and price. Also there is a pretty strong correlation with market cap and the count.This could be due to more tweets corresponding to more players getting into the market therefor expanding the market cap. The scatter plots with line regressions really show the positive correlation and vizulize how they are related. The count by price graphs is an even better vizualization of the data as it shows how closly the counts mimic the movement of the actual price. Now this can be infered in two ways though, did price move due to the number of tweets or did the number of tweets move due to the price. From the data it is hard to tell because it seems almost simultaniously. This partially could be due to markets being open 24/7 and trades being instantanous without restriction.  

From the information presented above, I concluded there is an correlation between the two, especially with Ethereum due to the bigger range of samples. These cryptocurrencies which are not bitcoin are colloquially referred to as "altcoins". From personal expeirence I beleive most alt coins act like etherum does with social media precense being a huge aspect in its price. Another factor to take into account is during the date range of the data, the big boom happend where Bitcoin went up to 17K within 30 days and gained international attention. I beleive that this boom and crash gained the attention of bigger players which is shaping the current market today. From my experience in trading these coins I found that alot of what happens in the cryptocurrency market does not follow general financial markets trends. The volatility of the market is so much higher so seeing this correlation of social media between coins and something like twitter is very intresting and raises questions on what other non-traditional aspects effect the price.  



# **Moving Forward**
Moving forward with this project I woud definintely want to incorporate NLP as one statistic to see if sentiment does have any affect. That would allow me to truely see if any publicity is good publicity. Another aspect I would like to investigate is to create a sort of traction metric from twitter retweets,likes and replys and other metrics associated with tweets to get a better idea of total "views". Also other social media platforms and news outlet publications must have an effect on the market also if there is a correlation with just twitter so analyzing them would also be intresting also. Ultimately I would move to create some sort of trading recomender based off of tweets inputted to truely see the functionally of this at work.

# **Photo and Data Credits/Sources**
## Picture sources
Title picture: https://www.reviewgeek.com/3603/best-bitcoin-and-cryptocurrency-price-tracking-apps/ 

## Datasets sources
 Pathak, Ajeet Ram (2019), “Social media data #bitcoin #Ethereum # facebook ”, Mendeley Data, v1 http://dx.doi.org/10.17632/chx9mdyydb.1 

Badiola, Jaime (2019), "Bitcoin 17.7 million Tweets and price", Kaggle Data, v2 https://www.kaggle.com/jaimebadiola/bitcoin-tweets-and-price/metadata

 Wilden, Chase (2017),"Cryptocurrency Price by Day/Hr (2013 - 2018) (w/Bitcoin)" , Data.World, Version: Updated as of 2019-07-31 https://data.world/chasewillden/cryptocurrency-price-by-date-2013-february-2018 