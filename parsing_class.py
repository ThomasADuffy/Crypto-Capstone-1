from pprint import pprint
import time
import json
import getpass
import numpy as np
import pandas as pd
from datetime import datetime

class coinmarketcap_jsonfile(object):

    def __init__(self,filename):
        with open(filename) as file:
            self.data = json.load(file)
        self.keys = list(self.data.keys())
        self.values= list(self.data.values())

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
        return self.data

    def parse_time_data(self):
        ''' This will take in the dataframe created by mege_df_on_time and reformate the time
        column into a date time objects.'''
        if isinstance(self.data, pd.DataFrame):
            self.data['time'] = self.data['time'].apply(lambda x :datetime.fromtimestamp(int(int(x)/1000)))
        else:
            self.merge_df_on_time()
            self.data['time'] = self.data['time'].apply(lambda x :datetime.fromtimestamp(int(int(x)/1000)))
        return self.data

    def print_min_max_datetime(self):
        
        print(f"The oldest tweet is: {min(self.data['time'])}")
        print(f"The youngest tweet is: {max(self.data['time'])}")

class crypto_csv_tweets(object):

    def __init__(self,filename):
        self.data = pd.read_csv(filename,error_bad_lines=False)
        self.clean_column_names()
        self.create_datetime_objects()
        
    def clean_column_names(self):
        colnames = self.data.columns.tolist()
        colnames = [col.lower().strip().replace(' ', '_') for col in colnames]
        self.data.columns = colnames

    def create_datetime_objects(self):
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])

    def print_min_max_datetime(self):
        print(f"The oldest tweet is: {min(self.data['datetime'])}")
        print(f"The youngest tweet is: {max(self.data['datetime'])}")

if __name__ == "__main__":
    pass
    

