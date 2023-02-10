import json
from datetime import datetime
from decouple import config
import pandas as pd
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key=config('NEWSAPIKEY'))

# /v2/top-headlines
top_tech = newsapi.get_top_headlines(category='technology', language='en', page_size=50)
top_sc = newsapi.get_top_headlines(category='science', language='en', page_size=50)

articles = top_tech["articles"] + top_sc["articles"]
df = pd.json_normalize(articles)

now = datetime.now()
datestr = now.strftime("%d%b-%H%M%S")

df.to_csv(f'scraped_news/{datestr}.csv')

print(f"Got {len(articles)} articles")
