import csv
import time
import re

import tweepy as tw

CONSUMER_KEY = '4GhvQSrvzjcFAbaO8JRT7dhMk'
CONSUMER_SECRET = '3sFNnC6BSonGW0TsKIEsB4tkS4voow5eldHqPW7nsgC7GRmuNL'
ACCESS_TOKEN = '2341867464-VK2hAtFRZMLBm8JsA1keEZTt4JhnCieiOXWf0cP'
ACCESS_TOKEN_SECRET = 'fZf4EzWGpdCjX0jNGejjXluxvXyhkbe4w5cpHZbbBQRhY'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAIAETwEAAAAAZ7Dlv5%2BvSt7AByWSAVrO%2BF0l2Jc' \
               '%3DKcoQGSBmO2ZoYXA8lJkPGD3O5Nm9PwuMYz4FqMk0gaIqahKxX4 '

KEYWORDS = ['Generative AI', 'SOTA', 'pytorch', 'keras', 'kaggle', 'LLM', 'GAN', 'large language models', 'GoogleAI',
            'ChatGPT', 'Data Scientist', 'Huggingface', 'kubernetes', 'fastai', 'deepmind', 'transformers', 'numpy',
            'tensorflow']

AUTHORS = ['AlphaSignalAI', 'RisingSayak', 'mrdbourke', 'keerthanpg', 'AiBreakfast', 'abacusai', 'dair_ai', 'Prathkum',
           'marktenenholtz', 'Jeande_d', 'svpino', 'mathemagic1an', 'art_zucker', 'itsandrewgao']


def main():
    # Authenticate to Twitter
    client = tw.Client(bearer_token=BEARER_TOKEN,
                       consumer_key=CONSUMER_KEY,
                       consumer_secret=CONSUMER_SECRET,
                       access_token=ACCESS_TOKEN,
                       access_token_secret=ACCESS_TOKEN_SECRET,
                       wait_on_rate_limit=True)

    # Create a tweet search query for keywords
    query = ' OR '.join(['({})'.format(keyword) for keyword in KEYWORDS])
    query += ' -is:retweet -is:reply -is:quote lang:en'

    # Create a tweet search query for authors
    # query_string = " OR ".join(["from:" + author for author in AUTHORS])
    # query = "(" + query_string + ") -is:retweet -is:reply -is:quote lang:en"

    # Search for tweets
    tweets = client.search_recent_tweets(query=query, max_results=10)
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

            # Create a dictionary representing the tweet
            obj = {'id': tweet.id,
                   'text': text,
                   'likes': client.get_liking_users(tweet.id).meta['result_count'],
                   "quotes": client.get_quote_tweets(tweet.id).meta['result_count'],
                   "retweets": client.get_retweeters(tweet.id).meta['result_count'],
                   }
            results.append(obj)  # Add the tweet to the results

    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Write the results to a CSV file
    with open(timestr + '-' + str(len(results)) + '.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    main()
