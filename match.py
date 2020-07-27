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
        self.soup = BeautifulSoup(requests.get(url).content, 'lxml')
    
    def get_batting_table(self, innings):
        tablesBatsmen = self.soup.find_all('table', attrs = {'class':'table batsman'})
        index = innings - 1
        return tablesBatsmen[index]
    
    def get_team(self, teamnum):
        tableBatsmen = self.get_batting_table(teamnum)
        team = []
        for b in tableBatsmen.find_all('a'):
            team.append(b.contents[0])
        return team

        
    
        
url = 'https://www.espncricinfo.com/ci/engine/match/1152839.html'
url2 = 'https://stats.espncricinfo.com/ci/engine/match/1225248.html'
# soup = BeautifulSoup(requests.get(url).content, 'lxml')
# tablesBatsmen = soup.find_all('table', attrs = {'class':'table batsman'})
# firstInns = tablesBatsmen[1].find_all('a')
# for b in firstInns:
#     print(b.contents[0])

match = Match(url)
# print(match.get_team(1))
# print(match.get_batting_table(1).prettify())
t = match.get_batting_table(1)
dfs = pd.read_html(url)

df = dfs[0]
df = df[df['BATSMEN'].notna()]

