"""Functions shared by Azure Functions"""

import json

def get_collection_link(db_id, collection_id):
    """Create and return collection link based on values passed in"""

    # Return a link to the relevant CosmosDB Container/Document Collection
    return "dbs/" + db_id + "/colls/" + collection_id


def get_cosmos_client(cosmosdb_uri, cosmosdb_key):
    from azure.cosmos import CosmosClient
    client = CosmosClient(cosmosdb_uri, cosmosdb_key)
    database = client.get_database_client("discoveruni")
    container = database.get_container_client("courses")
    return container


def get_http_error_response_json(error_title, error_key, error_value):
    """Returns a JSON object indicating an Http Error"""
    http_error_resp = {}
    http_error_resp["errors"] = []
    http_error_resp["errors"].append(
        {"error": error_title, "error_values": [{error_key: error_value}]}
    )
    return json.dumps(http_error_resp)
