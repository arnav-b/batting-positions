# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""    


import pandas as pd
from match import Match
import re

# Get matches

# import requests
# from bs4 import BeautifulSoup

# urls = []
# for n in range(1,10):
#     page = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;page={0};spanmin1=1+Jan+2010;spanval1=span;template=results;type=aggregate;view=match'.format(n)
    
#     r = requests.get(page)
#     soup = BeautifulSoup(r.content, 'lxml')
    
#     text = soup('a', text = re.compile(r'Match scorecard'))
#     for t in text:
#         urls.append('https://stats.espncricinfo.com' + t.get('href'))

# # Some test urls
url1 = 'https://www.espncricinfo.com/series/19430/scorecard/1187008/india-vs-south-africa-2nd-test-icc-world-test-championship-2019-2021'
url2 = 'https://www.espncricinfo.com/series/19297/scorecard/1187672/new-zealand-vs-england-2nd-test-england-in-new-zealand-2019-20'
url3 = 'https://www.espncricinfo.com/series/19497/scorecard/1225247/england-vs-west-indies-1st-test-west-indies-in-england-2020'
url4 = 'https://www.espncricinfo.com/series/13436/scorecard/387572/south-africa-vs-england-3rd-test-england-tour-of-south-africa-2009-10'
# urls = [url4, url1, url2, url3]

# matches = []
# for url in urls:
#     try:
#         match = Match(url)
#     except:
#         continue
# matches.append(match)

###############################################################################
# Get data on No. 3s and 4s
###############################################################################

data3 = []
data4 = []
# matches = []
testMatches = [Match(url4), Match(url1), Match(url2), Match(url3)]

for match in testMatches:
    print('Current match:', match)
    
    for innings in range(1, len(match.bat_dfs) + 1):
        print('Current innings:', innings)
        
        batdf = match.get_batting_df(innings)
        
        if len(batdf) >= 3:
            fow = re.split(':|\),', match.get_fow(innings))
            notOut = 1 if batdf.loc[3, 'Dismissal'] == 'not out' else 0
            
            innsData3 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[3, 'Batsman'], batdf.loc[3, 'R'], 
                        batdf.loc[3, 'B'], batdf.loc[3, 'M'], notOut, fow[4], 
                        fow[8], match.get_total(innings)]
            
            data3.append(innsData3)
        
        if len(batdf) >= 4:
            notOut = 1 if batdf.loc[4, 'Dismissal'] == 'not out' else 0
            
            innsData4 = [match.get_dates(), match.get_season(), 
                        match.get_match_number(), match.get_venue(), 
                        innings, batdf.loc[4, 'Batsman'], batdf.loc[4, 'R'], 
                        batdf.loc[4, 'B'], batdf.loc[4, 'M'], notOut, fow[13], 
                        fow[17],match.get_total(innings)]
            
            data4.append(innsData4)
            

cols = ['Dates', 'Season', 'Match No', 'Venue', 'Innings', 'Batsman', 'R', 'B', 
        'M', 'Not Out', 'FoWR', 'FoWO', 'Total']
df3 = pd.DataFrame(data3, columns=cols)
df4 = pd.DataFrame(data4, columns=cols)

df3.to_csv('df3.csv')
df4.to_csv('df4.csv')