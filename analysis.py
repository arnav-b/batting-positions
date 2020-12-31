import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Get data

df = pd.read_csv('df.csv')

# Overall distribution of fall of wickets 

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Runs)')
sns.distplot(df.FoWR1, ax=ax, label='First Wicket')
sns.distplot(df.FoWR2, ax=ax, label='Second Wicket')

fig, ax = plt.subplots()
ax.set_title('Fall of Wicket Distribution (Overs)')
sns.distplot(df.FoWO1, ax=ax, label='First Wicket')
sns.distplot(df.FoWO2, ax=ax, label='Second Wicket')

# Some scatterplots

fig, ax = plt.subplots()
sns.scatterplot(df.FoWR1, df.FoWR2 - df.FoWR1, hue=df.Innings)
plt.title('Second Wicket vs Opening Partnership')
plt.xlabel('Opening Partnership')
plt.ylabel('Second Wicket Partnership')
plt.show()

sns.scatterplot(df.FoWR1, df['3R'], hue=df.Innings)
plt.title('No 3 Score vs Opening Partnership')
plt.xlabel('Fall of First Wicket (R)')
plt.ylabel('No 3 Score')
plt.show()

sns.scatterplot(df.FoWR2, df['4R'], hue=df.Innings)
plt.title('No 4 Score vs Fall of Second Wicket')
plt.xlabel('Fall of Second Wicket (R)')
plt.ylabel('No 4 Score')
plt.show()

# Analysis for Smith 

dfSmith = df[(df['3Batsman'].str.contains('SPD Smith')) |\
             (df['4Batsman'].str.contains('SPD Smith'))]

dfSmith['SmithPosition'] = dfSmith['3Batsman'].apply(lambda x: 3 if 'SPD Smith' in x else 4)

# Comparing Smith to other Australian 3s and 4s
sns.catplot(x='SmithPosition', y='3R', hue='Innings', kind='box', data=dfSmith)
plt.xlabel('Smith Position')
plt.ylabel('Runs by the No 3')
plt.title('Smith vs Others at No 3')

sns.catplot(x='SmithPosition', y='4R', hue='Innings', kind='box', data=dfSmith)
plt.xlabel('Smith Position')
plt.ylabel('Runs by the No 4')
plt.title('Smith vs Others at No 4')

# Comparing Australia totals with Smith at 3 and 4
sns.catplot(x='SmithPosition', y='Total', hue='Innings', kind='box', data=dfSmith)
plt.title('Australian Totals with Smith at 3 and 4')
plt.show()

# Two-factor ANOVA for Smith's position and innings
sns.pointplot(x=dfSmith.Innings, y=dfSmith.Total, hue=dfSmith.SmithPosition)
plt.title('Interaction Plot for Australia Totals by Innings')
plt.show()

lmSmith = sm.formula.ols('Total ~ Innings + SmithPosition', data=dfSmith).fit()
aovSmith = sm.stats.anova_lm(lmSmith, typ=2)

res = lmSmith.resid
fig = sm.qqplot(res)
plt.title('QQ Plot of Residuals for Smith ANOVA Model')

# When does Smith come in?

fig, ax = plt.subplots()
ax.set(xlim=(0, 400))
sns.distplot(df[df['3Batsman'].str.contains('SPD Smith')].FoWR1, ax=ax,
             label = 'At 3')
sns.distplot(df[df['4Batsman'].str.contains('SPD Smith', na=False)].FoWR2, ax=ax,
             label = 'At 4')
plt.title('When Smith Comes in')
plt.xlabel('Fall of Wicket')

# Analysis for Root

dfRoot = df[(df['3Batsman'].str.contains('JE Root')) |\
             (df['4Batsman'].str.contains('JE Root'))]
dfRoot['RootPosition'] = dfRoot['3Batsman'].apply(lambda x: 3 if 'JE Root' in x else 4)

# Comparing Root to other English 3s and 4s

sns.catplot(x='RootPosition', y='3R', hue='Innings', kind='box', data=dfRoot)
plt.xlabel('Root Position')
plt.ylabel('Runs by the No 3')
plt.title('Root vs Others at No 3')

sns.catplot(x='RootPosition', y='4R', hue='Innings', kind='box', data=dfRoot)
plt.xlabel('Root Position')
plt.ylabel('Runs by the No 4')
plt.title('Root vs Others at No 4')

# Confidence intervals for Root at 3 and 4

ci_Eng3 = sm.stats.CompareMeans(sm.stats.DescrStatsW(dfRoot[dfRoot['RootPosition'] == 3]['3R']),
                                sm.stats.DescrStatsW(dfRoot[dfRoot['RootPosition'] == 4]['3R']))
print(ci_Eng3.tconfint_diff(usevar='unequal'))

ci_Eng4 = sm.stats.CompareMeans(sm.stats.DescrStatsW(dfRoot[dfRoot['RootPosition'] == 4]['4R']),
                                sm.stats.DescrStatsW(dfRoot[dfRoot['RootPosition'] == 3]['4R'].notna()))
print(ci_Eng4.tconfint_diff(usevar='unequal'))

# Comparing England totals with Root at 3 and 4
sns.catplot(x='RootPosition', y='Total', hue='Innings', kind='box', data=dfRoot)
plt.title('English Totals with Root at 3 and 4')
plt.show()

# Interaction plot for Root's position and innings
sns.pointplot(x='Innings', y='Total', hue='RootPosition', data=dfRoot)
plt.title('Interaction Plot for England Totals by Innings')
plt.show()

# Where does Root come in?

fig, ax = plt.subplots()
ax.set(xlim=(0, 200))
sns.distplot(df[df['3Batsman'].str.contains('JE Root')].FoWR1, ax=ax,
             label = 'At 3')
sns.distplot(df[df['4Batsman'].str.contains('JE Root', na=False)].FoWR2, ax=ax,
             label = 'At 4')
plt.title('When Root Comes in')
plt.xlabel('Fall of Wicket')
