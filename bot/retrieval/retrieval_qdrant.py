
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

# Access environment variables
from settings import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_EMBEDDINGS_MODEL = settings.OPENAI_EMBEDDINGS_MODEL




from logger import retrieval_logger

retrieval_logger.warning(f"Using OpenAI Embedding'{OPENAI_EMBEDDINGS_MODEL}'")


from langchain_openai.embeddings import OpenAIEmbeddings
embedding_function = OpenAIEmbeddings(model = OPENAI_EMBEDDINGS_MODEL,api_key=OPENAI_API_KEY)


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`

QDRANT_URL = settings.QDRANT_URL

retrieval_logger.warning(f"QDRANT_URL at '{QDRANT_URL}'")
client = QdrantClient(QDRANT_URL)

collection_name=settings.COLLECTION_NAME
DOCUMENTS_RETRIEVAL_LIMIT = settings.DOCUMENTS_RETRIEVAL_LIMIT


retrieval_logger.warning(f"collection_name {collection_name}")
retrieval_logger.warning(f"DOCUMENTS_RETRIEVAL_LIMIT {DOCUMENTS_RETRIEVAL_LIMIT}")


def retrieval_node(state: BotState):
    retrieval_logger.info(f"[{state['conversation_id']}] ---RETRIEVE---")

    query = state["messages"][-1].content
    vector = embedding_function.embed_query(query)
    
    results = client.query_points(collection_name, query=vector, limit=DOCUMENTS_RETRIEVAL_LIMIT)
    # print(results)
    # context="context:\n"
    # context += "\n ".join([r.payload["information"] for r in results.points])
    
    retrieved_documents= [r.payload["information"]for r in results.points]
    
    retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {len(retrieved_documents)} documents")
    retrieval_logger.info(f"[{state['conversation_id']}] {retrieved_documents}")
    return {"retrieved_documents": retrieved_documents}