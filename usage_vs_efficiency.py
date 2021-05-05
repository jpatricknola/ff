'''
Testing the correlation between usage and efficency for fantasy points
'''
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt

# import the csv
df = pd.read_csv('2019.csv')
# drop unneccessary columns
df.drop(['Rk', '2PM', '2PP', 'FantPt', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'], axis=1, inplace=True)
# rename some headers
df.rename({
'TD': 'PassingTD',
'TD.1': 'RushingTD',
'TD.2': 'ReceivingTD',
'TD.3': 'TotalTD',
'Yds': 'PassingYDs',
'Yds.1': 'RushingYDs',
'Yds.2': 'ReceivingYDs',
'Att': 'PassingAtt',
'Att.1': 'RushingAtt'
}, axis=1, inplace=True)
# get specific positions
rb_df = df[df['FantPos'] == 'RB']
qb_df = df[df['FantPos'] == 'QB']
wr_df = df[df['FantPos'] == 'WR']
te_df = df[df['FantPos'] == 'TE']

# get relevant data for positions
rushing_col = ['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD']
receiving_col = ['Tgt', 'Rec', 'ReceivingYDs', 'Y/R', 'ReceivingTD']
passing_col = ['PassingAtt', 'PassingYDs', 'PassingTD', 'Int']

# function for creating dataframe with dynamic columns
def transform_col(df, new_list):
    df = df[['Player', 'Tm', 'Age', 'G'] + new_list + ['FL']]
    return df

# create dataframes for position groups with relevant columns
rb_df = transform_col(rb_df, rushing_col + receiving_col)
wr_df = transform_col(wr_df, rushing_col + receiving_col)
te_df = transform_col(te_df, receiving_col)
qb_df = transform_col(qb_df, passing_col + rushing_col)

# add column for fantasy points based on scoring for relevant stats
rb_df['FantasyPoints'] = rb_df['RushingYDs']*0.1 + rb_df['RushingTD']*6 + rb_df['Rec'] + rb_df['ReceivingYDs']*0.1 + rb_df['ReceivingTD']*6 - rb_df['FL']*2
# add column for fantasy points per game based on scoring for relevant stats
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints']/rb_df['G']
rb_df['FantasyPoints/GM'] = rb_df['FantasyPoints/GM'].apply(lambda x: round(x, 2))
# add column for usage per game (rushing attempts and targets)
rb_df['Usage/GM'] = (rb_df['RushingAtt'] + rb_df['Tgt'])/rb_df['G']
rb_df['Usage/GM'] = rb_df['Usage/GM'].apply(lambda x: round(x, 2))
# add column for total fantasy points
df['FantasyPoints'] = (df['PassingYDs']*0.04) + df['PassingTD']*4 - df['Int']*2 + df['RushingYDs']*.1 + df['RushingTD']*6 + df['Rec'] + df['ReceivingYDs']*.1 + df['ReceivingTD']*6 - df['FL']*2
# add column for fantasy points per game
df['FantasyPoints/GM'] = df['FantasyPoints']/df['G']

# formatting for data plots
sns.set_style('whitegrid')
fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

# see correlation of usage in comparison to fantasy points
plot = sns.regplot(
x=rb_df['Usage/GM'],
y=rb_df['FantasyPoints/GM'],
scatter=True,)

# see correlation of efficiencyt to fantasy football performance
rb_df['Efficiency'] = (rb_df['RushingTD']+ rb_df['ReceivingTD'])/(rb_df['RushingAtt'] + rb_df['Tgt'])
fig, ax = plt.subplots()
fig.set_size_inches(15, 10)

#Make sure there is an adequete sample size
rb_df = rb_df[rb_df['RushingAtt'] > 20]

#plot that shit
plot = sns.regplot(
x=rb_df['Efficiency'],
y=rb_df['FantasyPoints/GM'],
scatter=True)
