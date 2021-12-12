import sqlite3

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def get_tweet():
    conn = sqlite3.connect('/code/db/tweets_db.db')
    cur = conn.cursor()
    cur.execute(
        'SELECT sentence FROM markovified_tweets_table ORDER BY RANDOM() LIMIT 1')
    tweet = cur.fetchone()[0]
    conn.close()
    return render_template('app.html', tweet=tweet)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
