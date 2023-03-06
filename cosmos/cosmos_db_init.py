import json
import azure.cosmos.cosmos_client as cosmos_client
from azure.cosmos import exceptions, PartitionKey
from azure.cosmos.exceptions import CosmosResourceExistsError

"""
create a resource group
create a azure cosmos db in the resource group
run cosmos_db_init.py
"""


def init():
    print('Imported packages successfully.')

    # Initialize the Cosmos client

    # URI/PRIMARY_KEY in : Azure Cosmos DB Account --> Settings --> Keys
    config = {
        "endpoint": "https://ytw-cosmos.documents.azure.com:443/",
        "primarykey": "IXFtnebOUiBI846pbqYjUymPIUDeIcX33zNi3zhlqSRzGIlmKNwGdmGMF7cnHVCMV90N9zSfYbE5ACDbEIffyw=="
    }

    # Create the cosmos client
    client = cosmos_client.CosmosClient(url=config["endpoint"], credential={"masterKey": config["primarykey"]})

    return client


def create_db(client):
    try:
        database = client.create_database(id=database_name)
        print(f"Database created: {database.id}")
    except exceptions.CosmosResourceExistsError:
        database = client.get_database_client(database=database_name)
        print("Database already exists.")

    return database


def create_container(database):
    try:
        partition_key_path = PartitionKey(path="/id")
        container = database.create_container(
            id='newsContainer',
            partition_key=partition_key_path,
            offer_throughput=400,
        )
        print(f"Container created: {container.id}")

    except CosmosResourceExistsError:
        print("Container already exists.")

    return container


if __name__ == '__main__':
    database_name = 'newsData'
    database_link = 'dbs/' + database_name
    client = init()
    database = create_db(client)
    container = create_container(database)
