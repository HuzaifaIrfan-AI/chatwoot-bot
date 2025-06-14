
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")




import logging
retrieval_logger=logging.getLogger("retrieval")

retrieval_logger.info(f"Using OpenAI Embedding'{OPENAI_EMBEDDINGS_MODEL}'")


from langchain_openai.embeddings import OpenAIEmbeddings
embedding_function = OpenAIEmbeddings(model = OPENAI_EMBEDDINGS_MODEL,api_key=OPENAI_API_KEY)


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`

Qdrant_URL = os.getenv("Qdrant_URL", "http://localhost:6333")
retrieval_logger.info(f"Qdrant_URL at '{Qdrant_URL}'")
client = QdrantClient(Qdrant_URL)

collection_name="middlehost"
MAX_DOCUMENTS_RETRIEVAL=3

def retrieval_node(state: BotState):
    retrieval_logger.info(f"[{state["conversation_id"]}] ---RETRIEVE---")
    
    query = state["messages"][-1].content
    vector = embedding_function.embed_query(query)
    
    results = client.query_points(collection_name, query=vector, limit=MAX_DOCUMENTS_RETRIEVAL)
    # print(results)
    # context="context:\n"
    # context += "\n ".join([r.payload["information"] for r in results.points])
    
    retrieved_documents= [r.payload["information"]for r in results.points]
    
    retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {len(retrieved_documents)} documents")
    # retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {retrieved_documents}")
    return {"retrieved_documents": retrieved_documents}