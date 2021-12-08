import tweepy

from utils.config import consumer_key, consumer_secret, access_token, access_token_secret


def tweepy_connect():
    # twitter api config
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)
