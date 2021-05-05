import requests
from bs4 import BeautifulSoup
import pandas as pd

ENDPOINT = "https://www.espn.com/nfl/stats/player/_/stat/rushing/table/rushing/sort/rushingYards/dir/desc"

# it comes with player and team in the same row, fix that
def format_team_and_player(df):
    # make an empty team column
    df['Team'] = ''
    for index, row in df.iterrows():
        # save the player name as a variable (with team in there)
        player = row['Name']
        team = ''
        # pop the uppercase letters off the end of player and save them as team
        while player[-1].isupper(): 
            team = player[-1] + team
            player = player[:-1]
        # when thats done, rewrite the name and team columns with updated values for the player
        df.loc[index, 'Name'] = player
        df.loc[index, 'Team'] = team
        
        # get the html
res = requests.get(ENDPOINT)

if res.ok:
    html = res.content
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    
    df_1 = pd.read_html(str(tables))[0]
    df_2 = pd.read_html(str(tables))[1]
    format_team_and_player(df_1)
    
    df = df_1.merge(df_2, left_index=True, right_index=True)
    df.reset_index(drop=True, inplace=True)
    
    df.to_csv('RB_2020.csv', index=False)


