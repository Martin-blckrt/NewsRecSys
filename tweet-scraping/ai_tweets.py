import csv
import time
import re
import csv

import tweepy as tw

CONSUMER_KEY = '4GhvQSrvzjcFAbaO8JRT7dhMk'
CONSUMER_SECRET = '3sFNnC6BSonGW0TsKIEsB4tkS4voow5eldHqPW7nsgC7GRmuNL'
ACCESS_TOKEN = '2341867464-VK2hAtFRZMLBm8JsA1keEZTt4JhnCieiOXWf0cP'
ACCESS_TOKEN_SECRET = 'fZf4EzWGpdCjX0jNGejjXluxvXyhkbe4w5cpHZbbBQRhY'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIAETwEAAAAAZ7Dlv5%2BvSt7AByWSAVrO%2BF0l2Jc' \
               '%3DKcoQGSBmO2ZoYXA8lJkPGD3O5Nm9PwuMYz4FqMk0gaIqahKxX4'

KEYWORD = True
ACCOUNT = False

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

def get_tag_from_tweet(tweet, keywords):
    pattern = re.compile("|".join(keywords), re.IGNORECASE)
    tweet_text = tweet.text.lower()
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

            res.append(obj)
        return res

    return None

def main():
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

    queries = []

    queries.append(f"({' OR '.join(KEYWORDS)}) -is:retweet -is:quote -is:reply lang:en")
    other = " OR ".join(["from:" + author for author in ACCOUNTS])
    others = "(" + other + ") -is:retweet -is:reply -is:quote lang:en"
    queries.append(others)

    results = []

    for i, query in enumerate(queries):

        choice = True if i == 1 else False

        # Search for tweets
        tweets = client.search_recent_tweets(query=query,
                                             max_results=10,
                                             expansions=['author_id', 'attachments.media_keys'],
                                             media_fields=['public_metrics'],
                                             tweet_fields=["public_metrics", 'created_at'])
        tweets_data = tweets.data

        results += [*get_data_from_search(client, tweets_data, KEYWORDS, choice)]

    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Write the results to a CSV file
    with open(timestr + '-' + str(len(results)) + '.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    main()
