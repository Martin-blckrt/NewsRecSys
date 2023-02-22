import pandas as pd
#import ai_tweets as twitter
#import reddit as reddit
#import gnews as gnews
#import fetch_newsapi as newsapi

if __name__ == '__main__':
    #twitter.main()
    #reddit.main()
    #gnews.main()
    #newsapi.main()

    df_reddit = pd.read_csv('reddit.csv')
    df_twitter = df_tweets = pd.read_csv('twitter.csv')
    df_gnews = pd.read_csv('gnews.csv')
    df_newsapi = pd.read_csv('news_api.csv')

    df_twitter['author'] = df_twitter['author'].astype(str)

    merged_1 = pd.merge(df_reddit, df_twitter, on=['author'], how='outer')
    merged_2 = pd.merge(merged_1, df_gnews, on=['title'], how='outer')
    merged_3 = pd.merge(merged_2, df_newsapi, on=['title', 'author'], how='outer')

    merged_3.to_csv('data.csv')
