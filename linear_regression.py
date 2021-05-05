import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import seaborn as sns; sns.set_style('whitegrid');

df = pd.read_csv("data_cleaned.csv")


# aggregated yearly data
df = df.groupby(['player_id', 'tm', 'player', 'pos', 'season'], as_index=False)\
    .agg({
    'offensive_snapcount': np.sum,
    'offensive_snapcount_percentage': np.mean,
    'passing_rating': np.mean,
    'passing_yds': np.sum,
    'passing_td': np.sum,
    'passing_att': np.sum,
    'receiving_yds': np.sum,
    'receiving_td': np.sum,
    'receiving_rec': np.sum,
    'receiving_tar': np.sum,
    'rushing_att': np.sum,
    'standard_fantasy_points': np.sum,
    'ppr_fantasy_points': np.sum,
    'half_ppr_fantasy_points': np.sum
})
    
print(df['season'].min(), df['season'].max())

# no snapcounts before 2012
df = df.loc[df['season'] >= 2012]

pd.set_option('chained_assignment', None)

# relevant things from previous years
lag_features = [
    'rushing_att', 
    'receiving_tar', 
    'offensive_snapcount', 
    'offensive_snapcount_percentage', 
    'ppr_fantasy_points', 
    'passing_rating', 
    'passing_att', 
    'passing_td'
    ]

for lag in range(1, 6):
    shifted = df.groupby('player_id').shift(lag)
    
    for column in lag_features:
        # example: lag_rushing_att_3 = what were rushing attempts 3 years ago
        df[f'lag_{column}_{lag}'] = shifted[column]
        
# if a player didnt play 5 years ago or whatever, give them -1
df = df.fillna(-1)




'''
split up our data in to 20% testing, 80% training
don't want to use the same data for testing as did for training (data leakage)
'''
wr_df = df.loc[(df['pos'] == 'WR') & (df['season'] < 2019)]
wr_df = wr_df.loc[wr_df['offensive_snapcount'] > 50]

X = wr_df[[
    'lag_receiving_tar_1', 'lag_offensive_snapcount_1', 'lag_ppr_fantasy_points_1'
]].values

y = wr_df['ppr_fantasy_points'].values

y = wr_df['ppr_fantasy_points'].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# sklearn.linear_model.LinearRegression documentation
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
lr = LinearRegression()

# train the algorithm
# the fit method documentation
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression.fit
lr.fit(X_train, y_train)

"""
Predicted values based off testing data. We are going to compare these predicted values to 
real world values and try to quantify the difference between our model and reality
"""
# predict method documentation
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression.predict
y_pred = lr.predict(X_test)

"""
A mean absolute error of 47 means our model was on average off by 47 fantasy points, or 3 points per game.
This is about what we'd expect from such a simple model.
"""
# mean_absolute_error documentation
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html
mean_absolute_error(y_pred, y_test)

pd.set_option('display.max_rows', None)

wr_df_pred = df.loc[
    (df['pos'] == 'WR') & (df['offensive_snapcount'] > 50) & (df['season'] == 2019), 
    ['player', 'receiving_tar', 'offensive_snapcount', 'ppr_fantasy_points']
]

wr_df_pred['predicted_2020'] = lr.predict(wr_df_pred[['receiving_tar', 'offensive_snapcount', 'ppr_fantasy_points']].values)

wr_df_pred.sort_values(by='predicted_2020', ascending=False).head(100)