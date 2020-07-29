# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 18:59:34 2020

@author: arnav
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

class Match(object):
    
    def __init__(self, url):
        self.url = url
        self.r = requests.get(url)
        self.soup = BeautifulSoup(self.r.content, 'lxml')
        self.bat_dfs = pd.read_html(self.r.content, attrs = {'class':'table batsman'})
        self.bowl_dfs = pd.read_html(self.r.content, attrs = {'class':'table bowler'})
        
    # def get_batting_table(self, innings):
    #     try:
    #         return self.batting_tables[innings - 1]
    #     except IndexError:
    #         raise IndexError('Innings does not exist')
    
    def get_batting_df(self, innings):
        df = pd.read_html(self.r.content, attrs = {'class':'table batsman'})
        
    
    def get_bowling_df(self, innings):
        return pd.read_html(self.r.content, attrs = {'class':'table bowler'})[innings - 1]
    
    ## This function doesn't work
    # def get_batting_team(self, innings):
    #     tableBatsmen = self.get_batting_table(innings)
    #     team = []
    #     for b in tableBatsmen.find_all('a'):
    #         team.append(b.contents[0])
    #     return team
    
    def get_venue(self):
        venue = self.soup.find('td', attrs = {'class':'font-weight-bold match-venue'})
        return venue.a.contents[0]
    
    
        
        
url_win = 'https://www.espncricinfo.com/ci/engine/match/1152839.html'
url_inns_win = 'https://stats.espncricinfo.com/ci/engine/match/1187008.html'
url_draw = 'https://stats.espncricinfo.com/ci/engine/match/1187672.html'

match_win = Match(url_win)
match_inns_win = Match(url_inns_win)
match_draw = Match(url_draw)

dfs = pd.read_html(match_draw.r.content, attrs = {'class':'table batsman'})
df1 = dfs[0]
df2 = dfs[2]

# print(len(match_inns_win.batting_tables))
# batting_table = match_inns_win.get_batting_table(1)
# for b in batting_table.find_all('a'):
#     print(b.contents)
# bowling_table = match_inns_win.get_bowling_table(1)

    

