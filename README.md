# f1_tweets_generator
Simple twitter data ETL project. It extracts tweets from 4 big Formula 1 journalists, preprocess it and load to SQLite database. Then, the texts are [markovified](https://github.com/jsvine/markovify), loaded to another table and randomly displayed by simple flask app.    The general architecture:
![image](https://user-images.githubusercontent.com/41913470/147856327-fdf2aeee-d70a-4684-861b-d314ea5c2124.png)

## Sample usage
From the topmost directory with docker-compose.yaml run:
```bash
docker-compose up -d
```
More about the project in the [blog post](https://blog.brozen.me/posts/tweets_generator/).
