# **Crypto-Captstone-1** <!-- omit in toc -->
### A study of the correlation between cryptocurrency tweets and price<!-- omit in toc -->  
![Title pic][title_pic]

[title_pic]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/imgs/Title-image.jpg
<!-- toc -->
# **Table of Contents** <!-- omit in toc -->
- [**Introduction**](#introduction)
- [**What's the data?**](#whats-the-data)
- [**Initial Question and Assumptions**](#initial-question-and-assumptions)
- [**EDA and Cleaning of Data**](#eda-and-cleaning-of-data)
- [**Visualization**](#visualization)
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
I'm using two Datasets. One data set contained raw json file data for all of the prices of all cryptocurrencies but in order to work with my twitter data set, I will only be using the Ethereum and Bitcion json files for financial data. The twitter dataset is actually very clean so minor manipulations were needed to get a dataframe representing truely what I wanted. One issue I ran into was the twitter data for Bitcoin from my original data setwas very non consistant and had many inconsistencies by date. Therefor I had to find another dataset for tweets for bitcoin which I ended up utilzing. I will go into this further in the [EDA Section.](#eda-and-cleaning-of-data)


# **Initial Question and Assumptions**
Before even doing cleaning I started out with some base line questions and assumptions. One of the biggest assumptions which shaped my EDA was about publicity and marketing. I've bet you've heard "All publicity is good publicity, as long as they spell your name right." or "Any publicity is good publicity". I belive this is very true in todays age especially due to the exponentially lowering constraints to move informatin around due to technological improvements. In the case of a new market like cryptocurrency I beleive this was ever so present so I approached my data with the main question.

><span style=font-size:1.1em;>What is the correlation between the count of tweets per day and price of each coin?</span>

# **EDA and Cleaning of Data**
I utilized two Jupyter notebooks to do my EDA. They are labeled respectively in the notebooks folder of my repository(one for the json file and one for the csv files). Within these notebooks, I loaded in the data and looked at all the information and started to formulate how to gather the data I wanted from these respective files. I realized the best way was to create a class so as I looked into each data set I started to write class's for each respective file type.

First I dove into the Json files which contained financial data scraped from coinmarketcap. These json files contain a single dictionary with four key headers: market_cap_by_available_supply, price_btc, price_usd, and volume_usd. Each one of these keys values was a a list of two item lists. After some reasearch I found out that the the first item in each of the lists was a unix time stamp with the second item being the actual value of the key. Therefor I wrote a class that would parse through each of these keys and populate a pandas dataframe with the unix time stamp (converted to a date time object) as a column and the values as the other columns.   

The resulting class is within the parsing_class python file labeled:
```python
class coinmarketcap_jsonfile(object)
```  

I then started to go through the csv files of the twitter data. Luckly the Ethereum twitter file was only one file to begin with so creating a class to clean the data and export it into a pandas dataframe much like the json files. The Bitcoin twitter data though was split up into 12 diffrent csv files. So I created a python csv merger program which is located in the csv_combiner python file.  
The code is as follows:  
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
After creating these class's I started to load in the data and one aspect I noticed espcially about the bitcoin twitter csv file is that it contained alot of inconsistancies. It seems that some most days didnt have any tweets, which was very trivial for what I was looking to accomplish.It also had a very small date range, which did not help either. Below is a graph which shows the original set of data where each bar is a day.  
![Messy BTC twitter data][og_btc_count_bar]

[og_btc_count_bar]:https://github.com/ThomasADuffy/Crypto-Capstone-1/blob/master/graphs/oldBTC_price_vs_tweets_linegraph_bar.png  

Therefor I found another dataset which contained the counts of tweets per hour for a larger time frame and was more consistant and utilized that for my bitcoin twitter data. The dataset was from kaggle and had the count for tweets per hour which contained bitcoin. since it was a csv, I was able to utlize the class I already had which made importing and cleaning it extremely easy. All I had to do for this data set was a groupy by and sum the counts so I could get a count by day.

The datasets used also had a very diffrent date range between the two coins. The dates for the financial data of the coins spaned from the start of coinmarketcap keeping track of the coin to 02/09/2018. Therefor I didnt really have any issue with the date range. The only parameter which restricted my dates was the range of time which the twitter data covered.  For Ethereum the  date range was from 08/07/2015 - 02/09/2018 for both data sets. With Bitcion the tweets only went as far back as 08/01/2017 - 02/09/2018  so it was a much shorter time frame.

The two EDA notebooks can be found [here.](https://github.com/ThomasADuffy/Crypto-Capstone-1/tree/master/notebooks)
# **Visualization**
After wrestling with the data, I was finally able to get it into a formate which I liked and was able to start plotting. I created a file called 
# **Photo and Data Credits/Sources**
## Picture sources
Title picture: https://www.reviewgeek.com/3603/best-bitcoin-and-cryptocurrency-price-tracking-apps/ 

## Datasets sources
 Pathak, Ajeet Ram (2019), “Social media data #bitcoin #Ethereum # facebook ”, Mendeley Data, v1 http://dx.doi.org/10.17632/chx9mdyydb.1 

Badiola, Jaime (2019), "Bitcoin 17.7 million Tweets and price", Kaggle Data, v2 https://www.kaggle.com/jaimebadiola/bitcoin-tweets-and-price/metadata

 Wilden, Chase (2017),"Cryptocurrency Price by Day/Hr (2013 - 2018) (w/Bitcoin)" , Data.World, Version: Updated as of 2019-07-31 https://data.world/chasewillden/cryptocurrency-price-by-date-2013-february-2018 