# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""    

import numpy as np
import pandas as pd
from match import Match
import re

# Get matches

import requests
from bs4 import BeautifulSoup

urls = []
for n in range(1,10):
    page = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page={0};spanmin1=1+Jan+2010;spanval1=span;template=results;type=aggregate;view=match'.format(n)
    
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'lxml')
    
    text = soup('a', text = re.compile(r'Match scorecard'))
    for t in text:
        urls.append('https://stats.espncricinfo.com' + t.get('href'))

matches = []
n = 0
for url in urls:
    try:
        match = Match(url)
        matches.append(match)
    except:
        continue
    n += 1 
    print('Loading match', n, 'of', len(urls))

###############################################################################
# Get data on No. 3s and 4s
###############################################################################

data3 = []
data4 = []

for match in matches:
    print('Current match:', match)
    
    for innings in range(1, len(match.bat_dfs) + 1):
        print('Current innings:', innings)
        
        batdf = match.get_batting_df(innings)
        
        if len(batdf) >= 3:
            m1 = batdf.loc[1, 'M']
            m2 = batdf.loc[2, 'M']
            m3 = batdf.loc[3, 'M']
            fow = re.split(':|\),', match.get_fow(innings))[1]
            try:
                fowR = int(re.split('-| ', fow)[2])
                fowO = float(re.split(' ', fow)[-2])
            except:
                fowR = fowO = np.nan
            fowM = min(m1, m2)
            notOut = 1 if batdf.loc[3, 'Dismissal'] == 'not out'\
                or batdf.loc[3, 'Dismissal'] == 'retired hurt' else 0
            
            
            innsData3 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[3, 'Batsman'], batdf.loc[3, 'R'], 
                        batdf.loc[3, 'B'], batdf.loc[3, 'M'], notOut, fowR, 
                        fowO, match.get_total(innings)]
            
            data3.append(innsData3)
        
        if len(batdf) >= 4:
            fow = re.split(':|\),', match.get_fow(innings))[2]
            try:
                fowR = int(re.split('-| ', fow)[2])
                fowO = float(re.split(' ', fow)[-2])
            except:
                fowR = fowO = np.nan
            if m3 < max(m1, m2):
                fowM = max(m1, m2)
            else:
                fowM = fowM + m3            
            notOut = 1 if batdf.loc[3, 'Dismissal'] == 'not out'\
                or batdf.loc[3, 'Dismissal'] == 'retired hurt' else 0
            
            innsData4 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[4, 'Batsman'], batdf.loc[4, 'R'], 
                        batdf.loc[4, 'B'], batdf.loc[4, 'M'], notOut, fowR, 
                        fowO, match.get_total(innings)]
            
            data4.append(innsData4)
            

cols = ['Dates', 'Season', 'MatchNo', 'Venue', 'Innings', 'Batsman', 'R', 'B', 
        'M', 'NotOut', 'FoWR', 'FoWO', 'Total']
df3 = pd.DataFrame(data3, columns=cols)
df4 = pd.DataFrame(data4, columns=cols)

df3[['MatchNo', 'Innings', 'R', 'B', 'M', 'NotOut', 'FoWR', 'FoWO', 'Total']]\
    .apply(pd.to_numeric, errors='coerce')

df3.to_csv('df3.csv', index=False)
df4.to_csv('df4.csv', index=False)