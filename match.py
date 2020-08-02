# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:59:34 2020

@author: arnav
"""

import requests
import pandas as pd
import numpy as np
from math import floor
from re import split

pd.options.mode.chained_assignment = None

class Match(object):
    
    def __init__(self, url):
        self.url = url
        self.r = requests.get(url)
        self.bat_dfs = pd.read_html(self.r.content, attrs = {'class':'table batsman'})
        self.bowl_dfs = pd.read_html(self.r.content, attrs = {'class':'table bowler'})
        self.details = pd.read_html(self.r.content, attrs = {'class': 'w-100 table match-details-table'})[0]
    
    def __str__(self):
        return self.get_match_number()
    
    def get_batting_df(self, innings):
        df = self.bat_dfs[innings - 1].dropna(how='all')
        
        if any('Did not bat' in b for b in df['BATSMEN']) and\
            any ('Extras' in b for b in df['BATSMEN']):
            df.drop(df.tail(4).index, inplace=True)
        elif any('Did not bat' in b for b in df['BATSMEN']) or\
            any ('Extras' in b for b in df['BATSMEN']):
            df.drop(df.tail(3).index, inplace=True)
        else:
            df.drop(df.tail(2).index, inplace=True)
       
        df.index = range(1, len(df) + 1)
        
        if 'M' in df.columns:
            df.drop(columns=['SR', 'Unnamed: 8', 'Unnamed: 9'], inplace=True)
            df.columns = ['Batsman', 'Dismissal', 'R', 'B','M', '4s', '6s']
            try:
                df.astype({'R':'int32', 'B':'int32', '4s':'int32', '6s': 'int32', 
                           'M':'int32'}, copy=False)
            except:
                pass
        else:
            df.drop(columns=['SR', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], 
                    inplace=True)
            df.columns = ['Batsman', 'Dismissal', 'R', 'B', '4s', '6s']
            df['M'] = [np.nan] * len(df)
            try:
                df.astype({'R':'int32', 'B':'int32', '4s':'int32', 
                        '6s': 'int32'}, copy=False)
            except:
                pass
        
        return df
        
    def get_bowling_df(self, innings):
        df = self.bowl_dfs[innings - 1].copy()
        return df
    
    def get_extras(self, innings):
        df = self.bat_dfs[innings - 1]
        extras = int(df.loc[df['BATSMEN'] == 'Extras']['R'])
        return extras
    
    def get_total(self, innings):
        df = self.bat_dfs[innings - 1]
        total = str(df.loc[df['BATSMEN'] == 'TOTAL']['R'])
        total = split('/| |\n', total)[4]
        return total
    
    def get_overs(self, innings):
        balls = self.get_batting_df(innings)['B'].sum() -\
            self.get_bowling_df(innings)['NB'].sum()
        overs = balls/6
        overs = int(str(floor(overs)) + '.' + str(int((overs - floor(overs)) * 6)))
        return overs
    
    def get_fow(self, innings):
        df = self.bat_dfs[innings - 1]
        fow = df['BATSMEN'].iloc[-1]
        return fow
    
    def get_venue(self):
        return self.details.loc[0,0]
    
    def get_toss(self):
        df = self.details
        toss = df.loc[df[0] == 'Toss'][1]
        return toss
    
    def get_series(self):
        df = self.details
        series = df.loc[df[0] == 'Series'][1]
        return series
    
    def get_potm(self):
        df = self.details
        potm = df.loc[df[0] == 'Player of the match'][1]
        return potm
        
    def get_pots(self):
        df = self.details
        pots = df.loc[df[0] == 'Player of the Series'][1]
        return pots
    
    def get_match_number(self):
        df = self.details
        num = str(df.loc[df[0] == 'Match number'][1])
        num = split(' |\n', num)[6]
        return num
    
    def get_season(self):
        df = self.details
        season = str(df.loc[df[0] == 'Season'][1])
        season = split(' |\n', season)[4]
        return season
    
    def get_dates(self):
        df = self.details
        dates = df.loc[df[0] == 'Match days'][1]
        dates = split('    |\(', str(dates))[1]
        return dates

# match = Match('https://www.espncricinfo.com/series/19430/scorecard/1187008/india-vs-south-africa-2nd-test-icc-world-test-championship-2019-2021')
# # # df = match.bat_dfs[1]
# # # fow = df['BATSMEN'].iloc[-1]
# # # fow = split(':|\(|-', fow)
# # # date = str(match.get_dates())
# # # date = split('    |\(', date)
# # print(match.get_dates())
# # list1 = [np.nan] * 5
# # print(list1)
# df = match.get_batting_df(1)
# # print(df.loc[4, 'M'])