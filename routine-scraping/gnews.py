import json
import urllib.request
from decouple import config
import pandas as pd


def main():
    apikey = config("GNEWSAPIKEY")
    category = "technology"
    url = f"https://gnews.io/api/v4/top-headlines?topic={category}&token={apikey}&lang=en&country=us&max=10"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]

        df = pd.json_normalize(articles)

        df.to_csv('gnews.csv')


if __name__ == '__main__':
    main()
