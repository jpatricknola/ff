import numpy as np
import pandas as pd

df = pd.read_csv("data_cleaned.csv")

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


from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

'''
split up our data in to 20% testing, 80% training
don't want to use the same data for testing as did for training (data leakage)
'''

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