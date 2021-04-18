'''
Get data from FantasyFootballDataPros website
'''
import pandas as pd
from bs4 import BeautifulSoup 
import requests

URL = 'https://www.fantasyfootballdatapros.com/table'

response = requests.get(URL)
soup = BeautifulSoup(response.content, 'html.parser')

# find table element in the html response
table = soup.find('table')

# turn the table into a dataframe
df = pd.read_html(str(table))[0]

# get only wrs
wr_df = df.loc[df['Pos'] == 'WR']
#keep only necessary columns for wide recievers
wr_df = wr_df[['Player', 'Tgt', 'ReceivingYds', 'ReceivingTD', 'FantasyPoints']]
wr_df.head(50)