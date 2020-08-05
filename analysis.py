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

df = pd.read_csv('df.csv')

# Overall distribution of fall of wickets 

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Runs)')
sns.kdeplot(df.FoWR1, ax=ax, label='First Wicket')
sns.kdeplot(df.FoWR2, ax=ax, label='Second Wicket')

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Overs)')
sns.kdeplot(df.FoWO1, ax=ax, label='First Wicket')
sns.kdeplot(df.FoWO2, ax=ax, label='Second Wicket')

fig, ax = plt.subplots()
ax.set_title('Partnership for First vs Second Wicket')
ax.set_xlabel('Opening Partnership (R)')
ax.set_ylabel('Second Wicket Parternship (R)')
sns.jointplot(x=df.FoWR1, y=df.FoWR2 - df.FoWR1, kind='scatter')

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

fig, ax = plt.subplots()
ax.set_title('Second Wicket vs Opening Partnership')
sns.scatterplot(x='FoWR1', y=df.apply(lambda x: x['FoWR2'] - x['FoWR1'], axis=1), 
                hue='Innings', ax=ax, data=df)
ax.set_xlabel('Opening Partnership')
ax.set_ylabel('Second Wicket Partnership')

fig, ax = plt.subplots()
ax.set_title('No 3 Score vs Opening Partnership')
sns.scatterplot(x='FoWR1', y='3R', hue='Innings', ax=ax, data=df)
ax.set_xlabel('Fall of First Wicket (R)')
ax.set_ylabel('No 3 Score')

fig, ax = plt.subplots()
ax.set_title('No 4 Score vs Fall of Second Wicket')
sns.scatterplot(x='FoWR2', y='4R', hue='Innings', ax=ax, data=df)
ax.set_xlabel('Fall of Second Wicket (R)')
ax.set_ylabel('No 4 Score')

# Analysis for Smith 

dfSmith = df[(df['3Batsman'].str.contains('SPD Smith')) |\
             (df['4Batsman'].str.contains('SPD Smith'))]
    
dfSmith['SmithPosition'] = dfSmith['3Batsman'].apply(lambda x: 3 if 'SPD Smith' in x else 4)
    
sns.catplot(x=dfSmith.SmithPosition.apply(lambda x: 'SPD Smith' if x == 3 else 'Others'),
            y='3R', hue='Innings', kind='box', data=dfSmith)   
plt.title('Smith vs Others at No 3')
    
# Averages by innings

def get_average(df, innings):
    df = df[df.Innings == innings]
    avg = np.sum(df.R) / np.sum(df.NotOut == 0)
    return avg
    

