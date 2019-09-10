from pprint import pprint
import time
import json
import getpass
import numpy as np
import pandas as pd
from datetime import datetime

class coinmarketcap_jsonfile(object):

    def __init__(self,filename):
        self.filename=filename
        with open(filename) as file:
            self.data = json.load(file)
        self.keys = list(self.data.keys())
        self.values= list(self.data.values())
        self.clean_data()

    def print_keys(self):
        for key in self.keys:
            print(key)

    def print_values(self):
        for value in self.values:
            print(value)

    def key_value_to_pd(self,key,value):
        ''' This will take the values and turn this into a pandas dataframe
        Input
        -------
        key - The key of the dictionary being passed in
        value- The values associated with that key
        Return
        -------
        df - A pandas dataframe corresponding to those with time split out'''

        lst1,lst2 = zip(*value)
        return pd.DataFrame.from_dict({"time":lst1,f"{key}_value":lst2})

    def merge_df_on_time(self):
        ''' This function takes the values and keys associated with the json file
        and returns a dataframe joined on the time column,
        it does this by if it is the first iteration in the for loop it will instantiate the data frame,
        then every iteration after that, it will merge it on time with the other values.

         Return
         -------
         df - a dataframe of all the values joined on the time metric.'''

        i=0
        for key,value in self.data.items():
            
            if i==0:
                df = self.key_value_to_pd(key,value)
                i+=1
            else:
                df=pd.merge(df,self.key_value_to_pd(key,value), on='time',how='left')
        self.data = df

    def parse_time_data(self):
        ''' This will take in the dataframe created by mege_df_on_time and reformate the time
        column into a date time objects.'''

        self.data['time'] = self.data['time'].apply(lambda x :datetime.fromtimestamp((int(int(x)/1000))))
        self.data['time'] = self.data['time'].dt.date
        

    def clean_data(self):
        '''This runs all of the cleaning functions in this class.'''

        self.merge_df_on_time()
        self.parse_time_data()

    def date_filter(self,startdate,enddate):
        ''' Note: startdate and enddate must be a string and formated like 2017-10-30'''
        self.data=self.data[(self.data['time'] > startdate) & (self.data['time'] < enddate)]

    def reset_data(self):
        '''Resets data to original state'''

        with open(self.filename) as file:
            self.data = json.load(file)

    def print_min_max_datetime(self):
        
        print(f"The oldest tweet is: {min(self.data['time'])}")
        print(f"The youngest tweet is: {max(self.data['time'])}")

class crypto_csv_tweets(object):

    def __init__(self,filename):
        self.filename=filename
        self.data = pd.read_csv(filename, error_bad_lines=False)
        self.clean_data()

    def reset_data(self):
        self.data = pd.read_csv(self.filename, error_bad_lines=False)
        
    def clean_column_names(self):
        colnames = self.data.columns.tolist()
        colnames = [col.lower().strip().replace(' ', '_') for col in colnames]
        self.data.columns = colnames

    def create_datetime_objects(self):
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        self.data['datetime'] = self.data['datetime'].dt.date

    def clean_data(self):
        ''' This just runs both of the functions to clean the data'''
        self.clean_column_names()
        self.create_datetime_objects()

    def date_filter(self,startdate,enddate):
        ''' Note: startdate and enddate must be a string and formated like 2017-10-30'''
        self.data=self.data[(self.data['datetime'] > startdate) & (self.data['datetime'] < enddate)] 

    def count_tweets_by_day(self):
        ''' This will return a dataframe with the date and the count of total tweets next to it'''

        df = self.data['datetime'].dt.value_counts().reset_index().sort_values('index').reset_index(drop=True)
        colnames = df.columns.tolist()
        colnames = ['time','count']
        df.columns = colnames
        return df

    def print_min_max_datetime(self):
        print(f"The oldest tweet is: {min(self.data['datetime'])}")
        print(f"The youngest tweet is: {max(self.data['datetime'])}")

if __name__ == "__main__":
    pass
    

