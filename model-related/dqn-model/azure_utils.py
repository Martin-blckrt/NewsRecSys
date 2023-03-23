import azure.cosmos.cosmos_client as cosmos_client


def client_init():
    # URI/PRIMARY_KEY in : Azure Cosmos DB Account --> Settings --> Keys
    config = {
        "endpoint": "https://news-rec-db.documents.azure.com:443/",
        "primarykey": "TkeewxqZmQf61VqBhsly4OQ0fh1DElNRstDdQNUiwtrFjH8YkZse2L1o8UhOKmENcMLDAFErhExxACDb171Y9A=="
    }

    # Create the cosmos client
    client = cosmos_client.CosmosClient(url=config["endpoint"], credential={"masterKey": config["primarykey"]})

    return client


def get_db(client, db_name):
    return client.get_database_client(database=db_name)


def get_container(db, c_name):
    return db.get_container_client(container=c_name)
