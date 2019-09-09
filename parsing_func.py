from pprint import pprint
import time
import json
import getpass
import numpy as np
import pandas as pd

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
        ''' This will take the values and turn this into a pandas dataframe'''
        lst1,lst2 = zip(*value)
        return pd.DataFrame.from_dict({"time":lst1,f"{key}_value":lst2})

    def merge_pd(self):
        ''' This func
        this by if it is the first iteration, to instantiate the data frame,
         then every iteration after that, it will merge it on time'''
        i=0
        for key,value in self.data.items():
            
            if i==0:
                df = self.key_value_to_pd(key,value)
                i+=1
            else:
                df=pd.merge(df,self.key_value_to_pd(key,value), on='time',how='left')
        return df
    def parse_time_data(self,df)


if __name__ == "__main__":
    btc=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/bitcoin.json")
    eth=coinmarketcap_jsonfile(f"/media/{getpass.getuser()}/extra/Crypto-Capstone-1/data/Json/ethereum.json")
    

