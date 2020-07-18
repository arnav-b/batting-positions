# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 19:30:59 2020

@author: arnav
"""

import urllib.request
import json

class TestMatch(object):
    def __init__(self, idnum):
        with urllib.request.urlopen('https://www.espncricinfo.com/ci/engine/match/' +\
                         str(idnum) + '.json') as url:
            data = json.loads(url.read().decode())
        self.id = idnum
        


idnums = [406200, 456669]
with urllib.request.urlopen('https://www.espncricinfo.com/ci/engine/match/' +\
                          str(idnums[0]) + '.json') as url:
    data = json.loads(url.read().decode())
    print(data.keys())
    print(data['innings'])
    print(data['centre']['common']['batting'])
    

from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.espncricinfo.com/series/13229/scorecard/456669/')
soup = BeautifulSoup(r.content, 'lxml')
# print(soup.prettify())

table = soup.find('table', attrs = {'class':'table batsman'})
# print(table.prettify())
for bat in table.findAll('td', attrs = {'class':'batsman-cell text-truncate out'}):
    print(bat.span)

