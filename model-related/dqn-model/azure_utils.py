import azure.cosmos.cosmos_client as cosmos_client


def client_init():
    # URI/PRIMARY_KEY in : Azure Cosmos DB Account --> Settings --> Keys
    config = {
        "endpoint": "https://ytw-cosmos.documents.azure.com:443/",
        "primarykey": "IXFtnebOUiBI846pbqYjUymPIUDeIcX33zNi3zhlqSRzGIlmKNwGdmGMF7cnHVCMV90N9zSfYbE5ACDbEIffyw=="
    }

    # Create the cosmos client
    client = cosmos_client.CosmosClient(url=config["endpoint"], credential={"masterKey": config["primarykey"]})

    return client


def get_db(client, db_name):
    return client.get_database_client(database=db_name)


def get_container(db, c_name):
    return db.get_container_client(container=c_name)
