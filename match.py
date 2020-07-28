# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:59:34 2020

@author: arnav
"""

import pandas as pd

pd.options.mode.chained_assignment = None

class Match(object):
    
    def __init__(self, url):
        self.url = url
        self.dfs = pd.read_html(url)
    
    def get_batting_df(self, innings):
        df = self.dfs[2 * (innings - 1)]
        df = df[df['BATSMEN'].notna()]  
        

url = 'https://www.espncricinfo.com/ci/engine/match/1152839.html'
url2 = 'https://stats.espncricinfo.com/ci/engine/match/1187016.html'

dfs = pd.read_html(url)
df = dfs[0]
df = df[df['BATSMEN'].notna()]
df.drop(['Unnamed: 8', 'Unnamed: 9'], 1, inplace=True)
df.drop(list(range(12,15)))
df.index = list(range(1,15))
# print(df)

dfs2 = pd.read_html(url2)
print(dfs2[5])

class Innings(object):
    
    def __init__(self, battingdf, bowlingdf):
        self.batdf = battingdf
        self.bowldf = bowlingdf
    
    def get_bat_df(self):
        df = self.batdf[self.batdf['BATSMEN'].notna()]
        df.drop(['Unnamed: 8', 'Unnamed: 9'], 1, inplace=True)
        df.drop(list(range(12,15)), inplace=True)
        df.index = list(range(1,15))
        return df
    
    def get_bowl_df(self):
        return self.bowldf
    
    def get_total(self):
        return int(self.battingdf.iat[12,2])
    
    def get_extras(self):
        return int(self.battingdf.iat[11,2])
    
    def get_fow(self):
        fow = self.battingdf.iat[13,0]
        return fow