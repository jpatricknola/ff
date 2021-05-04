from twitter_search import generate_tweets
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd 

    
def generate_sentiment_scores(player_name):
    data = {
        'name': player_name,
        'positive': 0,
        'negative': 0,
        'neutral': 0,
        'total_tweets': 0
    }
       
    tweets = generate_tweets(player_name)
        
    sid = SentimentIntensityAnalyzer()
        
    for tweet in tweets:
        polarity_score = sid.polarity_scores(tweet)
        
        data['positive'] += polarity_score.get('pos', 0)
        data['negative'] += polarity_score.get('negative', 0)
        data['neutral'] += polarity_score.get('neu')
        data['total_tweets'] += 1
        
    return data

print(generate_sentiment_scores("Michael Thomas"))

