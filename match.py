# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:59:34 2020

@author: arnav
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from math import floor

pd.options.mode.chained_assignment = None

class Match(object):
    
    def __init__(self, url):
        self.url = url
        self.r = requests.get(url)
        self.soup = BeautifulSoup(self.r.content, 'lxml')
        self.bat_dfs = pd.read_html(self.r.content, attrs = {'class':'table batsman'})
        self.bowl_dfs = pd.read_html(self.r.content, attrs = {'class':'table bowler'})
    
    def get_batting_df(self, innings):
        df = self.bat_dfs[innings - 1].dropna(how='all')
        if any('Did not bat' in b for b in df['BATSMEN']):
            df.drop(df.tail(4).index, inplace=True)
        else:
            df.drop(df.tail(3).index, inplace=True)
        df.index = range(1, len(df) + 1)
        if 'M' in df.columns:
            df.drop(columns=['SR', 'Unnamed: 8', 'Unnamed: 9'], inplace=True)
            df.columns = ['Batsman', 'Dismissal', 'R', 'B', 'M', '4s', '6s']
            df.astype({'R':'int32', 'B':'int32', 'M':'int32', '4s':'int32', 
                       '6s': 'int32'}, copy=False)
        else:
            df.drop(columns=['SR', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], inplace=True)
            df.columns = ['Batsman', 'Dismissal', 'R', 'B', '4s', '6s']
            df.astype({'R':'int32', 'B':'int32', '4s':'int32', 
                       '6s': 'int32'}, copy=False)
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
        total = int(df.loc[df['BATSMEN'] == 'TOTAL']['R'])
        return total
    
    def get_overs(self, innings):
        balls = self.get_batting_df(innings)['B'].sum() -\
            self.get_bowling_df(innings)['NB'].sum()
        overs = balls/6
        overs = int(str(floor(overs)) + '.' + str(int((overs - floor(overs)) * 6)))
        return overs
    
    def get_winner(self):
        return 1
    
    def get_venue(self):
        venue = self.soup.find('td', attrs = {'class':'font-weight-bold match-venue'})
        return venue.a.contents[0]
    
        
# url_win = 'https://www.espncricinfo.com/ci/engine/match/1152839.html'

# url_draw = 'https://stats.espncricinfo.com/ci/engine/match/1187672.html'
# url_win2 = 'https://stats.espncricinfo.com/ci/engine/match/1152846.html'


# match_win2 = Match(url_win2)

# match_draw = Match(url_draw)

# # dfs = pd.read_html(match_draw.r.content, attrs = {'class':'table batsman'})

# # df2 = dfs[2]

# url_inns_win = 'https://stats.espncricinfo.com/ci/engine/match/1187008.html'
# match_inns_win = Match(url_inns_win)

# match_win = Match(url_win)
# details = match_win.soup.find('table', attrs = {'class':'w-100 table match-details-table'})
# rows = details.find('tr')

# print(match_win.bat_dfs[0])

# df1 = match_win.get_batting_df(2)
# df2 = match_win.get_bowling_df(2)
# df1 = df1.astype({'B':'int32'})
# balls = df1['B'].sum() - df2['NB'].sum()
# overs = balls/6
# strOvers = str(floor(overs)) + '.' + str(int((overs - floor(overs)) * 6))
# print(strOvers)


# if any('Burns' in b for b in df1['BATSMEN']):
#     print('True')
# print(df1)
# df1.dropna(how='all', inplace=True)
# print(df1)
# df1.drop(df1.tail(4).index, inplace=True)
# df1.index = range(1, len(df1) + 1)
# print(df1)
# if 'M' in df1.columns:
#     df1.columns = ['Batsman', 'Dismissal', 'R', 'B', 'M', '4s', '6s', 'SR']
#     # print(df1)
#     df1.astype({'R':'int32', 'B':'int32', 'M':'int32', '4s':'int32', '6s': 'int32', 
#             'SR':'float64'}).dtypes
# else:
#     df1.drop(columns=['Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9'], inplace=True)
#     # print(df1)
#     df1.columns = ['Batsman', 'Dismissal', 'R', 'B', '4s', '6s', 'SR']
#     # print(df1)
#     df1.astype({'R':'int32', 'B':'int32', '4s':'int32', '6s': 'int32', 
#             'SR':'float64'}).dtypes
# print(df1)


# print(len(match_inns_win.batting_tables))
# batting_table = match_inns_win.get_batting_table(1)
# for b in batting_table.find_all('a'):
#     print(b.contents)
# bowling_table = match_inns_win.get_bowling_table(1)

    

