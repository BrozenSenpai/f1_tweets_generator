import pandas as pd
import numpy as np
import markovify


from utils.twitter_auth import tweepy_connect
from utils.sqlite_connector import connect_sqlite


def get_user_tweets(username: str, count: int) -> pd.DataFrame:
    try:
        # set connection with database
        conn = connect_sqlite()
        cur = conn.cursor()
    # get maximum id from tweets_table
        cur.execute(
            'SELECT MAX(id) FROM tweets_table WHERE name = ?', (username,))
    # save query result
        since_id = cur.fetchone()[0]
        conn.close()
    except:
        since_id = None
    # set connection with twitter api via tweepy
    api = tweepy_connect()
    # get last 200 tweets from the user's timeline with id higher than max id in database
    tweets = api.user_timeline(screen_name=username,
                               count=count, include_rts=False, tweet_mode='extended', since_id=since_id)
    # save tweets to pandas dataframe
    df = pd.DataFrame(data=[(tweet.id, tweet.full_text, username)
                            for tweet in tweets], columns=['id', 'tweets', 'name'])
    return df


def preprocess_tweets(df: pd.DataFrame) -> pd.DataFrame:
    # remove hastags and mentions
    df.tweets = df.tweets.replace("(@|#)[A-Za-z0-9_]+", "", regex=True)
    # remove urls
    df.tweets = df.tweets.replace(r"(http\S+|www.\S+)", "", regex=True)
    # remove multiple spaces
    df.tweets = df.tweets.replace(r"\s+", ' ', regex=True)
    # remove empty rows
    df.tweets = df.tweets.replace('', np.nan)
    df = df.dropna(axis=0, subset=['tweets'])
    return df


def load_tweets(df: pd.DataFrame) -> None:
    # set connection with database
    conn = connect_sqlite()
    cur = conn.cursor()
    # create table (if not exists) with tweets and with max id
    cur.execute(
        'CREATE TABLE IF NOT EXISTS tweets_table (id INT, tweets TEXT, name TEXT, CONSTRAINT primary_key_constraint PRIMARY KEY (id))')
    # append dataframe to the existing table
    df.to_sql('tweets_table', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


def markovify_tweets() -> pd.DataFrame:
    # set connection with database
    conn = connect_sqlite()
    # load tweets to dataframe
    df = pd.read_sql('SELECT tweets FROM tweets_table', conn)
    conn.close()
    # make a markov model
    model = markovify.NewlineText(df.tweets)
    # save 100 markovified sentences to dataframe
    df = pd.DataFrame((model.make_short_sentence(280)
                       for x in range(100)), columns=['sentence'])
    return df


def load_markovified_tweets(df: pd.DataFrame) -> None:
    # set connection with database
    conn = connect_sqlite()
    cur = conn.cursor()
    # create table if not exists
    cur.execute(
        'CREATE TABLE IF NOT EXISTS markovified_tweets_table(sentence TEXT)')
    # replace existing table
    df.to_sql('markovified_tweets_table', conn,
              if_exists='replace', index=False)
    conn.commit()
    conn.close()


def run() -> None:
    # run whole etl process
    journalists = ['andrewbensonf1', 'ChrisMedlandF1',
                   'adamcooperf1', 'eddstrawf1']
    df = pd.concat(map(lambda x: get_user_tweets(
        x, 200), journalists), ignore_index=True)
    #df  = pd.read_csv('test.csv', usecols=['id', 'tweets', 'name'])
    df = preprocess_tweets(df)
    load_tweets(df)
    df = markovify_tweets()
    load_markovified_tweets(df)


if __name__ == '__main__':
    run()
