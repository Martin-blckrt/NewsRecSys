import csv
import time
import re
import csv
import requests
import time
import datetime
from datetime import date

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


def setup():
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

    # add authorization to our headers dictionary
    return {**headers, **{'Authorization': f"bearer {TOKEN}"}}


def scrape(headers):
    res = {}

    with open('subreddits.csv', "r") as file:
        reader = csv.reader(file)
        data = [row[0] for row in reader]

    for sub in data:
        res[sub] = requests.get("https://oauth.reddit.com/r/" + sub + "/hot", headers=headers)

    return res


# add yonk if no selftext
def sort(data):
    results = []
    for sub in data:
        for post in data[sub].json()['data']['children']:
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


def log_to_csv(data):
    timestr = time.strftime("%Y%m%d-%H%M%S")

    with open(timestr + '-' + str(len(data)) + '.csv', 'w', newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == '__main__':
    headers = setup()
    data = scrape(headers=headers)
    res = sort(data)
    log_to_csv(res)
