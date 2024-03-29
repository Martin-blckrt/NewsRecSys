import subprocess

subprocess.run(["python3", "-m", "pip", "install", "azure-functions"])
subprocess.run(["python3", "-m", "pip", "install", "azure-cosmos"])
subprocess.run(["python3", "-m", "pip", "install", "newsapi-python"])
subprocess.run(["python3", "-m", "pip", "install", "pandas"])
subprocess.run(["python3", "-m", "pip", "install", "tweepy"])

import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos import exceptions, PartitionKey
from azure.cosmos.exceptions import CosmosResourceExistsError
import requests
import datetime
import pandas as pd
import tweepy as tw
from newsapi import NewsApiClient
import json
import urllib.request
import re
import numpy as np

"""
create a resource group
create a azure cosmos db in the resource group
"""


def get_tag_from_tweet(tweet, keywords):
    keywords = [item.lower() for item in keywords]
    pattern = re.compile("|".join(keywords), re.IGNORECASE)
    tweet_text = tweet.text.lower()
    tweet_text = tweet_text.replace('#', '')
    match = pattern.search(tweet_text)

    if match:
        return match.group(0)
    else:
        return ""


def get_data_from_search(client, tweets_data, KEYWORDS, bool_acc):
    # Get the tweet text
    if tweets_data is not None and len(tweets_data) > 0:

        res = []

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
                   "url": "https://twitter.com/i/web/status/" + str(tweet.id),
                   "time": tweet.created_at,
                   "source": "twitter",
                   "tag": str(tweet.author_id) if bool_acc else get_tag_from_tweet(tweet, KEYWORDS)
                   }

            if not bool_acc:
                if obj['likes'] > 0 or obj['retweets'] > 0 or obj['replies'] > 0 or obj['quotes'] > 0:
                    if obj['impressions'] > 100:
                        res.append(obj)
            else:
                res.append(obj)
                
        return res

    return None


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
                   '%3DKcoQGSBmO2ZoYXA8lJkPGD3O5Nm9PwuMYz4FqMk0gaIqahKxX4'

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
                "TDataScience",
                "towards_AI",
                "BBCTech",
                "dair_ai",
                "Prathkum",
                "mathemagic1an",
                "trending_repos",
                "patloeber",
                "CSProfKGD",
                "Michael_J_Black",
                "heyBarsee",
                "ptrblck_de",
                "rowancheung",
                "_geekculture_",
                "AI_PlainEnglish"]

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
                "tensorflow",
                "generativeai",
                'largelanguagemodels',
                'datascientist']

    queries = []

    queries.append(f"({' OR '.join(KEYWORDS)}) -is:retweet -is:quote -is:reply lang:en")
    other = " OR ".join(["from:" + author for author in ACCOUNTS])
    others = "(" + other + ") -is:retweet -is:reply -is:quote lang:en"
    queries.append(others)

    results = []
    choice = False

    for i, query in enumerate(queries):
        choice = True if i == 1 else False

        # Search for tweets
        tweets = client.search_recent_tweets(query=query,
                                             max_results=100,
                                             expansions=['author_id', 'attachments.media_keys'],
                                             media_fields=['public_metrics'],
                                             tweet_fields=["public_metrics", 'created_at'])
        tweets_data = tweets.data

        results += [*get_data_from_search(client, tweets_data, KEYWORDS, choice)]

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
        "endpoint": "https://news-rec-db.documents.azure.com:443/",
        "primarykey": "TkeewxqZmQf61VqBhsly4OQ0fh1DElNRstDdQNUiwtrFjH8YkZse2L1o8UhOKmENcMLDAFErhExxACDb171Y9A=="
    }

    # Create the cosmos client
    client = cosmos_client.CosmosClient(url=config["endpoint"], credential={"masterKey": config["primarykey"]})

    return client


def create_db(client):
    database_name = 'newsData'
    try:
        database = client.create_database(id=database_name)
        print(f"Database created: {database.id}")
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database=database_name)
        print("Database already exists.")

    return database


def create_container(database):
    container_name = 'newsContainer'
    try:
        partition_key_path = PartitionKey(path="/id")
        container = database.create_container(
            id=container_name,
            partition_key=partition_key_path,
            offer_throughput=400,
        )
        print(f"Container created: {container.id}")

    except CosmosResourceExistsError:
        container = database.get_container_client(container=container_name)
        print("Container already exists.")

    return container


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

    df_twitter['time'] = pd.to_datetime(df_twitter.time).dt.tz_localize(None)

    merged_social = pd.merge(df_reddit, df_twitter, on=['author', 'url', 'title', 'time', 'likes', 'source', 'tag'],
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
        exists = False
        # if no item exists with this url, insert the item
        for _ in container.query_items(
                query='SELECT * FROM c WHERE c.url="' + data_dict['url'] + '"',
                enable_cross_partition_query=True):
            exists = True
        if not exists:
            container.upsert_item(body=data_dict)
    print('Records inserted successfully.')


if __name__ == '__main__':
    client = init()
    database = create_db(client)
    container = create_container(database)
    df = getdata()
    upsert(df, container)
    """
    limitTime = str(datetime.datetime.today() - timedelta(days=4))
    for item in container.query_items(query='SELECT * FROM c WHERE c.time < "' + limitTime + '"',
                                      enable_cross_partition_query=True):
        container.delete_item(item, partition_key=item['id'])
    """
