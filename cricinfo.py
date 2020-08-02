# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""    


import pandas as pd
from match import Match
import re

# Get match URLs

# import requests
# from bs4 import BeautifulSoup


# urls = []
# for n in range(1,6):
#     page = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page={0};spanmax2=31+Jul+2020;spanmin2=31+Jul+2015;spanval2=span;template=results;type=aggregate;view=match'.format(n)
    
#     r = requests.get(page)
#     soup = BeautifulSoup(r.content, 'lxml')
    
#     text = soup('a', text = re.compile(r'Match scorecard'))
#     for t in text:
#         urls.append('https://stats.espncricinfo.com' + t.get('href'))

###############################################################################
# Get data on No. 3s and 4s
###############################################################################
url1 = 'https://www.espncricinfo.com/series/19430/scorecard/1187008/india-vs-south-africa-2nd-test-icc-world-test-championship-2019-2021'
url2 = 'https://www.espncricinfo.com/series/19297/scorecard/1187672/new-zealand-vs-england-2nd-test-england-in-new-zealand-2019-20'
url3 = 'https://www.espncricinfo.com/series/19497/scorecard/1225247/england-vs-west-indies-1st-test-west-indies-in-england-2020'

urls = [url1, url2, url3]

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
            
            innsData3 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[3, 'Batsman'], batdf.loc[3, 'R'], 
                        batdf.loc[3, 'B'], batdf.loc[3, 'M'], fow1, 
                        match.get_total(innings)]
            
            data3.append(innsData3)
        
        if len(batdf) >= 4:
            fow2 = re.split(':|\(|-', match.get_fow(innings))[4]
            
            innsData4 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[4, 'Batsman'], batdf.loc[4, 'R'], 
                        batdf.loc[4, 'B'], batdf.loc[4, 'M'], fow2, 
                        match.get_total(innings)]
            
            data4.append(innsData4)
            

cols = ['Dates', 'Season', 'Match No', 'Venue', 'Innings', 'Batsman', 'R', 'B', 
        'M', 'FoW', 'Total']
df3 = pd.DataFrame(data3, columns=cols)
df4 = pd.DataFrame(data4, columns=cols)

df3.to_csv('df3.csv')
df4.to_csv('df4.csv')
