import http.client
import json
from datetime import datetime
from decouple import config
import pandas as pd


conn = http.client.HTTPSConnection("bing-news-search1.p.rapidapi.com")

headers = {
    'X-BingApis-SDK': "true",
    'X-RapidAPI-Key': config('RAPIDAPIKEY'),
    'X-RapidAPI-Host': "bing-news-search1.p.rapidapi.com"
}

conn.request("GET", "/news?textFormat=Raw&safeSearch=Moderate&category=Technology", headers=headers)


res = conn.getresponse().read().decode("utf-8")
jres = json.loads(res)
df = pd.json_normalize(jres)

# pd.set_option('display.max_colwidth', None)

now = datetime.now()
datestr = now.strftime("%d%b-%H%M%S")

df.to_csv(f'scraped_news/{datestr}.csv')
