# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""    

import requests
from bs4 import BeautifulSoup
from re import compile 

r = requests.get('https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;spanmax1=18+Jul+2020;spanmin1=18+Jul+2019;spanval1=span;template=results;type=aggregate;view=results')
soup = BeautifulSoup(r.content, 'lxml')

urls = []
text = soup('a', text = compile(r'Match scorecard'))
for t in text:
    urls.append('https://stats.espncricinfo.com' + t.get('href'))

url = urls[0]





