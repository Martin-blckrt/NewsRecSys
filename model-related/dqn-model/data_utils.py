import pandas as pd
from azure_utils import client_init, get_db, get_container


def load_dataset(local: bool) -> pd.DataFrame:
    if local:
        news_df = pd.read_csv("data/file.csv", header=None)

        news_df.columns = ['id', 'source', 'tag', 'title', 'description', 'author', 'url', 'likes',
                           'downs', 'time', 'tweet_id', 'followers', 'quotes', 'retweets',
                           'replies', 'impressions', 'image', 'content', 'source.url', '_rid',
                           '_self', '_etag', '_attachments', '_ts']
        return news_df
    else:
        return load_db_dataset()


def load_history(user_id: str, local: bool) -> list:
    if local:
        user_df = pd.read_csv("data/file.csv", header=None)
        user_df.columns = ['id', 'read_history']
        user_df.drop_duplicates(subset=["id"], keep="last", inplace=True, ignore_index=True)

        hist = user_df.loc[user_df['id'] == user_id]
    else:
        hist = load_db_history(user_id)

    # TODO: get (source, tag) kind of infos from news id
    return hist


def load_db_dataset() -> pd.DataFrame:
    client = client_init()
    database = get_db(client, "newsData")
    container = get_container(database, "newsContainer")

    item_list = list(container.read_all_items())

    print('Found {0} items'.format(item_list.__len__()))

    # convert to pandas dataframe
    return pd.DataFrame.from_records([r for r in item_list])


def load_db_history(user_id) -> list:
    client = client_init()
    database = get_db(client, "newsData")
    container = get_container(database, "userContainer")

    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.id=@id",
        parameters=[
            {"name": "@id", "value": user_id}
        ],
        enable_cross_partition_query=True
    ))

    print('Item queried by Id {0}'.format(items[0].get("id")))

    return items[0].get("read_history")


def sync_history(user_id, hist):
    client = client_init()
    database = get_db(client, "newsData")
    container = get_container(database, "userContainer")

    items = list(container.query_items(
        query="SELECT * FROM r WHERE r.id=@id",
        parameters=[
            {"name": "@id", "value": user_id}
        ],
        enable_cross_partition_query=True
    ))

    read_item = items[0]
    old_hist = read_item["read_history"]
    read_item["read_history"] = hist

    response = container.replace_item(item=read_item, body=read_item)

    print('Replaced Item\'s Id is {0}, old history={1}, new history={2}'.format(response['id'], old_hist,
                                                                                response['read_history']))


"""
Little scripts for Azure CosmoDB tests

fake_hist = ["12", "6"]
sync_history(user_id="1", hist=fake_hist)
"""
