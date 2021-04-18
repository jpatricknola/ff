
'''
Expert Consensus Rankings are an average of rankings from a large amount of experts 
for each player for a given season or week. 
We are clustering players in to tiers based on average expert rankings for the draft.
Using the KMeans algorithm which requires us to input the number of clusters
so we use silhoutte analysis to determine what number of clusters to input
'''
import pandas as pd
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns; sns.set_style('whitegrid')

# sorted list of all fantasy players ranked by average Expert Consensus Ranking
DATA_CSV = "https://raw.githubusercontent.com/fantasydatapros/data/master/fantasypros/ecr/PPR_ECR.csv"


# import the csv, remove missing values
df = pd.read_csv(DATA_CSV, index_col=0).dropna()

# In a 12 team, 16 spot league the draft pool is 192 players.
# adding the next 20 spots to account for free agent pickups post-draft
# so the dataframe will consist of the top ranked 212 players 
num_teams = 12
num_roster_spots = 16
draft_pool = num_teams * num_roster_spots + 20
df = df[:draft_pool]

'''
Use silhouette analysis to determine the k value (number of clusters) to be used for KMeans algorithm 
The silhouette value is a measure of how similar an object is to its own cluster (cohesion) 
compared to other clusters (separation). 
The silhouette ranges from −1 to +1, higher value indicates that the object 
is well matched to its own cluster and poorly matched to neighboring clusters.
'''

avgs = []

# we want at least 4 tiers, and not a whole fuckton, so stopping at 25
start = 4 
stop = 25

for n_clusters in range(start, stop):
    # taking the average ranking for players
    X = df[['Avg']].values
    
    # instantiate the kmeans model with hyperparameters
    model = KMeans(n_clusters=n_clusters) 
    
    # fit the model
    model.fit(X) 
    
    # assign the data points to clusters
    clusters = model.predict(X) 
    
    # calculate the silhouette avg for our clusters
    silhouette_avg = silhouette_score(X, clusters) 
    
    # append it to the list
    avgs.append(silhouette_avg) 

# if we want to see a graph of silhouette scores for all of them
plt.plot(np.arange(start, stop, 1), avgs)
plt.xlabel('Number of clusters')
plt.ylabel('Silhouette score')

# or we can just take the highest one
k_number = avgs.index(max(avgs)) + start

'''
Now that we have the k number, we can use k means algorithm
'''

pd.set_option('display.max_rows', None)

# again, using the average ranking, do a kmeans algorithm with the best k value
X = df[['Avg']].values
model = KMeans(n_clusters=k_number)
model.fit(X)
labels = model.predict(X)

# the kmeans algorithm assigns random labels to each cluster
# which means we have to map those labels to tiers

def assign_tiers(labels):
    unique_labels = []
    tiers = []
    
    for i in labels:
        if i not in unique_labels: unique_labels.append(i)
        tiers.append(
            len(set(unique_labels))
        )
    return tiers

# map labels -> tiers
tiers = assign_tiers(labels)
# create a new column for tiers
df['Tier'] = tiers
df.set_index('Tier').head()

def clustering_visualization(df, position=None, figsize=(20, 40)):
  # if a position is provided, only take players from that position
  # cant check for equivalency because positions are RB1, RB2, etc so just use contains
  if position:
    df = df.loc[df['Pos'].str.contains(position)]
  
  # list of distinct colors
  colors = ['purple', 'magenta', 'red', 'blue', 'orange', 'green',
    'salmon', 'yellow', 'black', 'grey', '#3498db', '#16a085', '#f4d03f', '#f1948a',
    '#48c9b0', '#3498db', '#e74c3c', '#d7bde2', '#d0d3d4'
  ]
  
  # map tiers to colors in a dictionary
  colors = dict(zip(range(1, k_number+1), colors[:k_number]))
  
  plt.figure(figsize=figsize)
  plt.scatter(
    x=df['Avg'],
    y=df['Rank'],
    c="#212f3d", #color
    alpha=0.9, #opacity
    s=7 #size
  )
  
  yticks = []
  
  for _index, row in df.iterrows():
    # on x axis show the player's range from highest to lowest expert ranking
    xmin = row['Best']
    xmax = row['Worst']
    # y axis just by rank
    ymin, ymax = row['Rank'], row['Rank']
    # player's name and tier
    player = row['Player']
    tier = row['Tier']
    
    plt.plot(
      (xmin, xmax), (ymin, ymax), c=colors.get(tier, 'black'), alpha=0.8
    )
    yticks.append(player)
    
  patches = []
  for tier, color in colors.items():
    patch = mpatches.Patch(color=color, label=f'Tier {tier}')
    patches.append(patch)
  
  # styles for visualization
  plt.legend(handles=patches, borderpad=1, fontsize=12)
  # labeling the axis
  plt.xlabel('Avg Expert Rank', fontsize=12)
  plt.ylabel('Expert Consensus Rank', fontsize=12)
  # make lines for each rank
  plt.yticks(df['Rank'], yticks, fontsize=12)
  # make number 1 be from top down
  plt.gca().invert_yaxis()
  plt.show()
