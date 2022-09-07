import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics
from typing import List

from secrets import consumer_key, consumer_secret

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_tweets(keyword: str) -> List[str]:
    all_tweets = []
    print(f"-> GETTING TWEETS [{keyword}]...")

    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang='en').items(100):
        all_tweets.append(tweet.full_text)
    
    #print(all_tweets, "\n")

    return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]:
    tweets_clean = []
    print(f"-> CLEANING...")
    
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))

    #print(tweets_clean, "\n")

    return tweets_clean

def get_sentiment(all_tweets: List[str]) -> List[float]:
    sentiment_scores = []
    print(f"-> TAKING SCORES...")
    
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)

    #print(sentiment_scores, "\n")

    return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score

if __name__ == "__main__":
    print("Whats does the World prefer?")
    first_thing = input()
    print("...or...")
    second_thing = input()
    print('\n')

    first_score = generate_average_sentiment_score(first_thing)
    print("\n")
    second_score = generate_average_sentiment_score(second_thing)
    print("\n")

    print("-> CALCULATING AVERAGES...")
    print(f"{first_thing} score: {first_score}")
    print(f"{second_thing} score: {second_score}")

    print('\n')

    if (first_score > second_score):
        print(f"The humanity prefers {first_thing} over {second_thing}!\n")
    else:
        print(f"The humanity prefers {second_thing} over {first_thing}!\n")