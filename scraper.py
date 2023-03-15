import csv
import requests
import datetime
import pandas as pd
import tweepy as tw
from decouple import config
from newsapi import NewsApiClient
import json
import urllib.request

def reddit():
    CLIENT_ID = '6diVRhNTByDRS0H1aoWkiw'
    SECRET_TOKEN = 'CbyVa6RA_fRRlGlJyKgecPx8xEHa1A'
    USERNAME = 'TheMightyNivor'
    PASSWORD = 'c^2mQU522&Py*R'

    CRITERIA = {'technology': {'score': 20, 'num_comments': 0},
                'realtech': {'score': 5, 'num_comments': 0},
                'tech': {'score': 20, 'num_comments': 0},
                'futurology': {'score': 700, 'num_comments': 0}}

    USEFUL_DATA = ['subreddit',
                   'selftext',
                   'title',
                   'author',
                   'score',
                   'num_reports',
                   'num_comments',
                   'url',
                   'created_utc']

    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_TOKEN)

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'YourTechWaveBot'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']

    res = {}

    with open('subreddits.csv', "r") as file:
        reader = csv.reader(file)
        data = [row[0] for row in reader]

    for sub in data:
        res[sub] = requests.get("https://oauth.reddit.com/r/" + sub + "/hot", headers={**headers, **{'Authorization': f"bearer {TOKEN}"}})

    results = []
    for sub in res:
        for post in res[sub].json()['data']['children']:
            if ((
                        datetime.date.fromtimestamp(
                            int(post['data']['created_utc']) + (24 * 60 * 60))) >= datetime.date.today()) & (
                    post['data']['stickied'] == False) & (post['data']['selftext'] != ""):
                for feature in USEFUL_DATA:
                    if feature in CRITERIA[sub]:
                        if post['data'][feature] < CRITERIA[sub][feature]:
                            continue

                obj = {'subreddit': post['data']['subreddit'],
                       'link_flair_text': post['data']['link_flair_text'],
                       'title': post['data']['title'],
                       'selftext': post['data']['selftext'],
                       'author': post['data']['author'],
                       'url': post['data']['url'],
                       'ups': post['data']['ups'],
                       'downs': post['data']['downs']
                       }
                results.append(obj)
    return results


def twitter():
    CONSUMER_KEY = '4GhvQSrvzjcFAbaO8JRT7dhMk'
    CONSUMER_SECRET = '3sFNnC6BSonGW0TsKIEsB4tkS4voow5eldHqPW7nsgC7GRmuNL'
    ACCESS_TOKEN = '2341867464-VK2hAtFRZMLBm8JsA1keEZTt4JhnCieiOXWf0cP'
    ACCESS_TOKEN_SECRET = 'fZf4EzWGpdCjX0jNGejjXluxvXyhkbe4w5cpHZbbBQRhY'
    BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIAETwEAAAAAZ7Dlv5%2BvSt7AByWSAVrO%2BF0l2Jc' \
                   '%3DKcoQGSBmO2ZoYXA8lJkPGD3O5Nm9PwuMYz4FqMk0gaIqahKxX4 '

    KEYWORD = False
    ACCOUNT = True

    # Authenticate to Twitter
    client = tw.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET,
                       wait_on_rate_limit=True)

    data = []

    if KEYWORD:
        # Create a tweet search query for keywords
        with open('keywords.csv', "r") as file:
            reader = csv.reader(file)
            data = [row[0] for row in reader]

        query = ' OR '.join(['({})'.format(keyword) for keyword in data])
        query += ' -is:retweet -is:reply -is:quote lang:en'
    else:
        # Create a tweet search query for authors
        with open('accounts.csv', "r") as file:
            reader = csv.reader(file)
            data = [row[0] for row in reader]

        query_string = " OR ".join(["from:" + author for author in data])
        query = "(" + query_string + ") -is:retweet -is:reply -is:quote lang:en"

    # Search for tweets
    tweets = client.search_recent_tweets(query=query,
                                         max_results=10,
                                         expansions=['author_id', 'attachments.media_keys'],
                                         media_fields=['public_metrics'],
                                         tweet_fields=["public_metrics"])
    results = []
    tweets_data = tweets.data

    # Get the tweet text
    if tweets_data is not None and len(tweets_data) > 0:
        for tweet in tweets_data:
            # Clean the text
            text = tweet.text
            substitutions = [("\n+", " "), (" +", " ")]
            for search, replace in substitutions:
                text = re.sub(search, replace, text)

            author_metrics = client.get_user(id=tweet.author_id, user_fields=['public_metrics'])

            # Create a dictionary representing the tweet
            obj = {'id': tweet.id,
                   'author': tweet.author_id,
                   'followers': author_metrics.data.public_metrics['followers_count'],
                   'text': text,
                   'likes': tweet.public_metrics['like_count'],
                   "quotes": tweet.public_metrics['quote_count'],
                   "retweets": tweet.public_metrics['retweet_count'],
                   "replies": tweet.public_metrics['reply_count'],
                   "impressions": tweet.public_metrics['impression_count']
                   }
            results.append(obj)  # Add the tweet to the results

    return results


def newsapi():
    newsapi = NewsApiClient(api_key=config('NEWSAPIKEY'))

    # /v2/top-headlines
    top_tech = newsapi.get_top_headlines(category='technology', language='en', page_size=50)
    top_sc = newsapi.get_top_headlines(category='science', language='en', page_size=50)

    articles = top_tech["articles"] + top_sc["articles"]
    return articles


def gnews():
    apikey = config("GNEWSAPIKEY")
    category = "technology"
    url = f"https://gnews.io/api/v4/top-headlines?topic={category}&token={apikey}&lang=en&country=us&max=10"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

    return articles


if __name__ == '__main__':
    df_reddit = pd.DataFrame(reddit())
    df_twitter = pd.DataFrame(twitter())
    df_newsapi = pd.DataFrame(newsapi())
    df_gnews = pd.DataFrame(gnews())

    df_twitter['author'] = df_twitter['author'].astype(str)

    merged_1 = pd.merge(df_reddit, df_twitter, on=['author'], how='outer')
    merged_2 = pd.merge(merged_1, df_gnews, on=['title'], how='outer')
    df = pd.merge(merged_2, df_newsapi, on=['title', 'author'], how='outer')
