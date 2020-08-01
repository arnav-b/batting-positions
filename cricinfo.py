# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""    


import pandas as pd
import seaborn as sns
from match import Match

# Get match URLs

import requests
from bs4 import BeautifulSoup
import re

urls = []
for n in range(1,6):
    page = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page={0};spanmax2=31+Jul+2020;spanmin2=31+Jul+2015;spanval2=span;template=results;type=aggregate;view=match'.format(n)
    
    r = requests.get(page)
    soup = BeautifulSoup(r.content, 'lxml')
    
    text = soup('a', text = re.compile(r'Match scorecard'))
    for t in text:
        urls.append('https://stats.espncricinfo.com' + t.get('href'))

###############################################################################
# Get data on No. 3s and 4s
###############################################################################

data3 = []
data4 = []

for url in urls:
    try:
        match = Match(url)
    except:
        continue
    print('Current match:', match)
    
    for innings in range(1, len(match.bat_dfs) + 1):
        print('Current innings:', innings)
        
        batdf = match.get_batting_df(innings)
        
        if len(batdf) >= 3:
            fow1 = re.split(':|\(|-', match.get_fow(innings))[2]
            
            innsData3 = [match.get_season(), match.get_match_number(), 
                        match.get_venue(), innings, batdf.loc[3, 'Batsman'], 
                        batdf.loc[3, 'R'], batdf.loc[3, 'B'], fow1, 
                        match.get_total(innings)]
            if 'M' in batdf.columns:
                innsData3s.append(batdf.loc[3, 'M'])
            else:
                innsData3s.append('N/A')
            
            data3.append(innsData3)
        
        if len(batdf) >= 4:
            fow2 = re.split(':|\(|-', match.get_fow(innings))[4]
            
            innsData4 = [match.get_season(), match.get_match_number(), 
                        match.get_venue(), innings, batdf.loc[4, 'Batsman'], 
                        batdf.loc[4, 'R'], batdf.loc[4, 'B'], fow2, 
                        match.get_total(innings)]
            if 'M' in batdf.columns:
                innsData4.append(batdf.loc[4, 'M'])
            else:
                innsData4.append('N/A')
            
            data4.append(innsData4)
            

cols = ['Season', 'Match No', 'Venue', 'Innings', 'Batsman', 'R', 'B', 'FoW', 
        'Total', 'M']
df3s = pd.DataFrame(data3s, columns=cols)

