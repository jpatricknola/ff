# Using a correlation matrix, determine which positions have most closely correlated performance

import pandas as pd
import numpy as np
import seaborn as sns; sns.set_style('whitegrid')
from matplotlib import pyplot as plt

# initalize empty data frame
df = pd.DataFrame()

# address for published CSV FF data 
WEEKLY_BASE_URL = "https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{year}/week{week}.csv"

year = 2019

# 17 weeks in a season
for week in range(1, 18):
  # read_csv accepts a url or a filepath
  weekly_df = pd.read_csv(WEEKLY_BASE_URL.format(year=year, week=week))
  # add a week column
  weekly_df['Week'] = week
  # concatenate into df on line 4
  df = pd.concat([df, weekly_df])
  
# output of print(df['Pos'].unique()):  
# ['QB' 'WR' 'RB' 'DB/LB' 'HB' 'TE' 'FB' 'WR/RS' 'WR/PR' 'FB/DL' 'C' 'CB'
#  'DB' 'OL' 'G/C' 'S' 'FB/TE' 'K' 'T' 'P' 'FS' 'G' 'CB/RS' 'C/G' 'LS' 'G/T'
#  'LB' 'T/G' 'DL' 'FB/RB' 'DT']. 

# combine redundant positions   
df = df.replace({
  'Pos': {
    'HB': 'RB',
    'WR/RS': 'WR',
    'WR/PR': 'WR',
    'FB/TE': 'TE',
    'FB/RB': 'RB'
  }
})

# take only the skill positions 
skill_positions = ['WR', 'TE', 'RB', 'QB']
df = df.loc[df['Pos'].isin(skill_positions)]

# take only the columns we need
columns = ['Player', 'Tm', 'Pos', 'Week', 'PPRFantasyPoints']
formatted_df = df[columns]
# treat rows with same player name + team name + position as one player, collapsing all weeks into 1 row.
# (can't group by player id because there is no id column in the data)
# put the weekly average in PPRF column
formatted_df = df.groupby(['Player', 'Tm', 'Pos'], as_index=False).agg({
  'PPRFantasyPoints': np.mean
})

# how many per position do we want to look at per team
position_map = {
  'QB': 1,
  'RB': 2,
  'WR': 4,
  'TE': 2
}

# returns the player at a given depth and position for each team
def get_players_by_position_and_depth(df, position, depth):
  pos_df = df.loc[df['Pos'] == position]
  return pos_df.groupby('Tm', as_index=False).apply(
    lambda dataframe: dataframe.nlargest(depth, ['PPRFantasyPoints']).min()
  )

# initalize new empty dataframe for correlation matrix
corr_df = pd.DataFrame()

for position, spots in position_map.items():
  for n in range(1, spots+1):
    # make a new dataframe players at that position and depth
    pos_df = get_players_by_position_and_depth(formatted_df, position, n)
    # change name of column to reflect the position+depth
    pos_df = pos_df.rename({'PPRFantasyPoints': f'{position}{n}'}, axis=1)
    # concatenate on the column (position+depth) instead of the row (team)
    corr_df = pd.concat([corr_df, pos_df], axis=1)
    
# drop all columns except the one that has pos_depth as name with value of FFPoints
corr_df = corr_df.drop(['Pos', 'Player', 'Tm'], axis=1)
print(corr_df.shape)

# visualization

plt.figure(figsize=(10, 7))
# dataframe.corr uses pearson correlation equation by default
# annot will make it show the number, cmap
sns.heatmap(corr_df.corr(), annot=True, cmap=sns.diverging_palette(0, 250))