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
        return df

    def parse_time_data(self):
        ''' This will take in the dataframe created by mege_df_on_time and reformate the time
        column into a date time objects.'''
        df = self.merge_df_on_time()
        df['time'] = df['time'].apply(lambda x :datetime.fromtimestamp(int(int(x)/1000)))
        return df

class csv_cleaner(object):

    def __init__(self,filename):
        self.data = pd.read_csv(filename,error_bad_lines=False)
        self.clean_column_names()
        
    def clean_column_names(self):
        colnames = self.data.columns.tolist()
        colnames = [col.lower().strip().replace(' ', '_') for col in colnames]
        self.data.columns = colnames


if __name__ == "__main__":
    btc=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/bitcoin.json")
    eth=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/ethereum.json")
    

