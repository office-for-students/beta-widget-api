import os
import logging
from azure.cosmos import CosmosClient

# class DataSetHelper:
#     def __init__(self, client, collection_link):
#         self.client = client
#         self.collection_link = collection_link

def get_highest_successful_version_number(cosmosdb_uri, cosmosdb_key):
    client = CosmosClient(cosmosdb_uri, cosmosdb_key)
    database = client.get_database_client("discoveruni")
    container = database.get_container_client("datasets")
    query = "SELECT VALUE MAX(c.version) from c WHERE c.status = 'succeeded'"
    max_version_number_list = list(
        container.query_items(query=query, enable_cross_partition_query=True, max_item_count=1)
    )
    version = max_version_number_list[0]
    logging.info(f"Highest successful dataset version: {version}")
    return version
