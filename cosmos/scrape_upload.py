import azure.cosmos.cosmos_client as cosmos_client
import requests
import datetime
import pandas as pd
import tweepy as tw
from newsapi import NewsApiClient
import json
import urllib.request
import re
import numpy as np


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

    SUBREDDITS = ["technology",
                  "realtech",
                  "tech",
                  "futurology"]

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

    for sub in SUBREDDITS:
        res[sub] = requests.get("https://oauth.reddit.com/r/" + sub + "/hot",
                                headers={**headers, **{'Authorization': f"bearer {TOKEN}"}})

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

                obj = {'source': post['data']['subreddit'],
                       'tag': post['data']['link_flair_text'],
                       'title': post['data']['title'],
                       'description': post['data']['selftext'],
                       'author': post['data']['author'],
                       'url': post['data']['url'],
                       'likes': post['data']['ups'],
                       'downs': post['data']['downs'],
                       'time': datetime.datetime.fromtimestamp(int(post['data']['created_utc']))
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

    ACCOUNTS = ["AlphaSignalAI",
                "RisingSayak",
                "mrdbourke",
                "keerthanpg",
                "AiBreakfast",
                "abacusai",
                "dair_ai",
                "Prathkum",
                "marktenenholtz",
                "Jeande_d",
                "svpino",
                "mathemagic1an",
                "art_zucker",
                "itsandrewgao",
                "sama",
                "trending_repos",
                "RisingSayak",
                "patloeber",
                "tunguz",
                "quantumVerd",
                "FrnkNlsn",
                "SchmidhuberAI",
                "CSProfKGD",
                # "ccanonne_",
                # "Michael_J_Black",
                # "heyBarsee",
                # "ptrblck_de",
                "mervenoyann"]

    KEYWORDS = ["Generative AI",
                "SOTA",
                "pytorch",
                "keras",
                "kaggle",
                "LLM",
                "GAN",
                "large language models",
                "GoogleAI",
                "ChatGPT",
                "Data Scientist",
                "Huggingface",
                "kubernetes",
                "fastai",
                "deepmind",
                "transformers",
                "numpy",
                "tensorflow"]

    data = []

    if KEYWORD:
        # Create a tweet search query for keywords
        query = ' OR '.join(['({})'.format(keyword) for keyword in KEYWORDS])
        query += ' -is:retweet -is:reply -is:quote lang:en'
    else:
        # Create a tweet search query for authors
        query_string = " OR ".join(["from:" + author for author in ACCOUNTS])
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
            obj = {'tweet_id': tweet.id,
                   'author': str(tweet.author_id),
                   'followers': author_metrics.data.public_metrics['followers_count'],
                   'title': text,
                   'likes': tweet.public_metrics['like_count'],
                   "quotes": tweet.public_metrics['quote_count'],
                   "retweets": tweet.public_metrics['retweet_count'],
                   "replies": tweet.public_metrics['reply_count'],
                   "impressions": tweet.public_metrics['impression_count'],
                   "url": "fakeTwitterURL",
                   "time": datetime.datetime.now(),
                   "source": "twitter"
                   }
            results.append(obj)  # Add the tweet to the results

    return results


def newsapi():
    newsapi = NewsApiClient(api_key="f54af54ed2164805824348bfaac1d534")

    # /v2/top-headlines
    top_tech = newsapi.get_top_headlines(category='technology', language='en', page_size=50)
    top_sc = newsapi.get_top_headlines(category='science', language='en', page_size=50)

    articles = top_tech["articles"] + top_sc["articles"]
    ndf = pd.json_normalize(articles)

    return ndf


def gnews():
    apikey = "1f956a6b862d056eda8a3b62f3fc4c9b"
    category = "technology"
    url = f"https://gnews.io/api/v4/top-headlines?topic={category}&token={apikey}&lang=en&country=us&max=10"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        gdf = pd.json_normalize(articles)

    return gdf


def init():
    print('Imported packages successfully.')

    # Initialize the Cosmos client

    # URI/PRIMARY_KEY in : Azure Cosmos DB Account --> Settings --> Keys
    config = {
        "endpoint": "https://ytw-cosmos.documents.azure.com:443/",
        "primarykey": "IXFtnebOUiBI846pbqYjUymPIUDeIcX33zNi3zhlqSRzGIlmKNwGdmGMF7cnHVCMV90N9zSfYbE5ACDbEIffyw=="
    }

    # Create the cosmos client
    client = cosmos_client.CosmosClient(url=config["endpoint"], credential={"masterKey": config["primarykey"]})

    return client


def getdata():
    df_reddit = pd.DataFrame(reddit())
    df_twitter = pd.DataFrame(twitter())
    df_newsapi = pd.DataFrame(newsapi())
    df_gnews = pd.DataFrame(gnews())

    df_newsapi = df_newsapi.rename(columns={"source.name": "source",
                                            "source.id": "source.url",
                                            "urlToImage": "image",
                                            "publishedAt": "time"})

    df_gnews = df_gnews.rename(columns={"source.name": "source",
                                        "publishedAt": "time"})

    merged_social = pd.merge(df_reddit, df_twitter, on=['author', 'url', 'title', 'time', 'likes', 'source'],
                             how='outer')
    merged_news = pd.merge(df_newsapi, df_gnews,
                           on=['title', 'url', 'time', 'source', 'description', 'content', 'source.url', 'image'],
                           how='outer')

    merged_news['time'] = merged_news['time'].apply(
        lambda x: datetime.datetime.strptime(x.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S'))

    df = pd.merge(merged_social, merged_news, on=['title', 'url', 'time', 'description', 'author', 'source'],
                    how='outer')

    df['time'] = df['time'].astype(str)
    df = df.reset_index()
    df = df.rename(columns={'index': 'id'})
    df['id'] = df['id'].astype(str)
    df = df.replace(np.nan, 0)

    return df


def upsert(df, container):
    # Write rows of a pandas DataFrame as items to the Database Container
    for i in range(0, df.shape[0]):
        # create a dictionary for the selected row
        data_dict = dict(df.iloc[i, :])
        container.upsert_item(body=data_dict)
    print('Records inserted successfully.')


if __name__ == '__main__':
    client = init()
    database = client.get_database_client('newsData')
    container = database.get_container_client('newsContainer')
    df = getdata()
    upsert(df, container)

    # upsert/create/replace/read/read_all/conflict
