import json
import urllib.request
from datetime import datetime
from decouple import config
import pandas as pd


apikey = config("GNEWSAPIKEY")
category = "technology"
url = f"https://gnews.io/api/v4/top-headlines?topic={category}&token={apikey}&lang=en&country=us&max=10"

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

    df = pd.json_normalize(articles)

    now = datetime.now()
    datestr = now.strftime("%d%b-%H%M%S")

    df.to_csv(f'scraped_news/{datestr}.csv')
