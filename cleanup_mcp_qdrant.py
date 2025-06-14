# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)


from qdrant_client import QdrantClient

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`
client = QdrantClient("http://localhost:6333")
collection_name="mcp_middlehost"

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)
    print(f"'{collection_name}' collection deleted")
else:
    print(f"'{collection_name}' collection not exist")