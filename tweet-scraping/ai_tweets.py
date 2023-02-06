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
               '%3DKcoQGSBmO2ZoYXA8lJkPGD3O5Nm9PwuMYz4FqMk0gaIqahKxX4 '

KEYWORD = False
ACCOUNT = True


def main():
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

    timestr = time.strftime("%Y%m%d-%H%M%S")

    # Write the results to a CSV file
    with open(timestr + '-' + str(len(results)) + '.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)


if __name__ == '__main__':
    main()
