from config import Config
from requests_oauthlib import OAuth1, OAuth1Session
import requests
import pprint
from urllib import parse

config = Config()

def generate_oauth_token():
  token = OAuth1(config.TWITTER_API_KEY, config.TWITTER_API_SECRET, config.USER_ACCESS_TOKEN, config.USER_ACCESS_SECRET)
  return token

PARAMS = {
  'lang': 'en',
  'count': '100',
  'include_entities': False
}

def generate_tweets(player_names, analysts=config.ANALYSTS):
  token = generate_oauth_token()
  
  from_accounts = 'from:'
  for i, account in enumerate(analysts.values()):
    if i == 0:
      from_accounts = from_accounts + account
    else:
      from_accounts = from_accounts + ' OR ' + account
      
  search_values = ''
  for i, val in enumerate(player_names):
    if i == 0:
      search_values = search_values + val
    else:
      search_values = search_values + ' OR ' + val
  
  search_query = parse.quote(search_values)
  url = config.TWITTER_SEARCH_URL + search_query
  print(url, "RULLL")
  res = requests.get(url, params=PARAMS, auth=token)
  print(res.text)
  
  tweets = res.json().get('statuses')
  parsed_tweets = []
  
  for tweet in tweets:
    truncated = tweet.get('truncated')
    text = tweet.get('text')
    if not truncated and not 'RT' in text:
      parsed_tweets.append(text)
  
  return parsed_tweets
  
print(generate_tweets(['Michael Thomas']))