# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 22:56:43 2020

@author: arnav
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from math import floor

# Get data

df3 = pd.read_csv('df3.csv')
df4 = pd.read_csv('df4.csv')

df3.drop('Unnamed: 0', axis=1, inplace=True)
df4.drop('Unnamed: 0', axis=1, inplace=True)



# Overall distribution of fall of wickets 

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Runs)')
sns.kdeplot(df3.FoWR, ax=ax, label='First Wicket')
sns.kdeplot(df4.FoWR, ax=ax, label='Second Wicket')

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Overs)')
sns.kdeplot(df3.FoWO, ax=ax, label='First Wicket')
sns.kdeplot(df4.FoWO, ax=ax, label='Second Wicket')

# fig, ax = plt.subplots()
# ax.set_title('Fall of Wicket Distribution (Minutes)')
# sns.kdeplot(df3.FoWM, ax=ax, label='First Wicket')
# sns.kdeplot(df4.FoWM, ax=ax, label='Second Wicket')

def get_fow_runs(df, innings='all'):
    if innings != 'all':
        df = df[df.Innings == innings]
    avg = np.sum(df.FoWR) / len(df)
    return avg

def get_fow_overs(df, innings='all'):
    if innings != 'all':
        df = df[df.Innings == innings]
    avg = np.sum(df.FowO) / len(df)
    return avg

# Some scatterplots

# sns.jointplot(x=df3.FoWR, y=df3.Total, kind='scatter')

# Averages by innings

def get_average(df, innings):
    df = df[df.Innings == innings]
    avg = np.sum(df.R) / np.sum(df.NotOut == 0)
    return avg
    

