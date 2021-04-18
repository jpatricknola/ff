import requests
from bs4 import BeautifulSoup
import pandas as pd

ENDPOINT = "https://www.espn.com/nfl/stats/player/_/stat/rushing/table/rushing/sort/rushingYards/dir/desc"

res = requests.get(ENDPOINT)

def format_team_and_player(df):
    df['Team'] = ''
    for index, row in df.iterrows():
        player = row['Name']
        team = ''
        while player[-1].isupper(): 
            team = player[-1] + team
            player = player[:-1]

        df.loc[index, 'Name'] = player
        df.loc[index, 'Team'] = team

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


