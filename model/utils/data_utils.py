import pandas as pd
import numpy as np
from model.utils.azure_utils import client_init, get_db, get_container


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


def load_history(user_id: str, local: bool) -> tuple:
    if local:
        user_df = pd.read_csv("data/file.csv", header=None)
        user_df.columns = ['id', 'read_history']  # state history ?
        user_df.drop_duplicates(subset=["id"], keep="last", inplace=True, ignore_index=True)

        hist = user_df.loc[user_df['id'] == user_id]
        st_hist = None
    else:
        hist, st_hist = load_db_history(user_id)

    return hist, st_hist


def load_db_dataset() -> pd.DataFrame:
    client = client_init()
    database = get_db(client, "newsData")
    container = get_container(database, "newsContainer")

    item_list = list(container.read_all_items())

    print('Found {0} news'.format(item_list.__len__()))

    # convert to pandas dataframe
    df = pd.DataFrame.from_records([r for r in item_list])
    df['tag'] = np.where(df['tag'] == 0, 'article', df['tag'])
    df['tag'] = df['tag'].replace(0, np.nan).replace('', np.nan)
    return df


def load_db_history(user_id) -> tuple:
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

    if len(items) == 0:
        history = []
        state_history = []

        print("Created new user " + user_id)

    else:
        history = items[0].get("read_history")
        state_history = items[0].get("state_history")

        print("Found {0} news in user's history".format(len(history)))

    return history, state_history


def sync_history(user_id, hist, st_hist):
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

    if len(items) == 0:
        read_item = {"id": user_id, "read_history": hist, "state_history": st_hist}
        container.create_item(body=read_item)
    else:
        read_item = items[0]
        # old_hist = read_item["read_history"] useful only for prints
        read_item["read_history"] = hist
        read_item["state_history"] = st_hist

        response = container.replace_item(item=read_item, body=read_item)

    print(f'User {user_id} history updated')


"""
Little scripts for Azure CosmoDB tests

fake_hist = ["12", "6"]
sync_history(user_id="1", hist=fake_hist)
"""
