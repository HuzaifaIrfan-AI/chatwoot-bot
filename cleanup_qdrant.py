

from qdrant_client import QdrantClient

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`
import os

from settings import settings
QDRANT_URL = settings.QDRANT_URL

client = QdrantClient(QDRANT_URL)
collection_name="rag"

if client.collection_exists(collection_name=collection_name):
    client.delete_collection(collection_name=collection_name)
    print(f"'{collection_name}' collection deleted")
else:
    print(f"'{collection_name}' collection not exist")