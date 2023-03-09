import pandas as pd
from pydocumentdb import document_client


def load_dataset(local: bool):
    if local:
        return load_local_dataset("data/file.csv")
    else:
        return load_db_dataset()


def load_local_dataset(path):
    news_df = pd.read_csv(path, header=None)

    news_df.columns = ['id', 'source', 'tag', 'title', 'description', 'author', 'url', 'likes',
                       'downs', 'time', 'tweet_id', 'followers', 'quotes', 'retweets',
                       'replies', 'impressions', 'image', 'content', 'source.url', '_rid',
                       '_self', '_etag', '_attachments', '_ts']

    news_df.drop_duplicates(subset=["id", "title"], keep="last", inplace=True, ignore_index=True)

    return news_df


def load_db_dataset():
    # set up Cosmos DB connection
    uri = 'https://ytw-cosmos.documents.azure.com:443/'
    key = 'IXFtnebOUiBI846pbqYjUymPIUDeIcX33zNi3zhlqSRzGIlmKNwGdmGMF7cnHVCMV90N9zSfYbE5ACDbEIffyw=='
    client = document_client.DocumentClient(uri, {'masterKey': key})

    # build the query
    query = {'query': 'SELECT * FROM c'}

    # execute the query
    options = {'enableCrossPartitionQuery': True}
    results = list(client.QueryDocuments('dbs/newsData/colls/newsContainer/', query, options=options))

    # convert to pandas dataframe
    return pd.DataFrame.from_records([r for r in results])
