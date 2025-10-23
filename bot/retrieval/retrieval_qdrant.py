

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

# Access environment variables
from settings import settings



from logger import retrieval_logger

# retrieval_logger.warning(f"Using OpenAI Embedding'{OPENAI_EMBEDDINGS_MODEL}'")


from vectorize_qdrant import collection_name, embedding_function, client



DOCUMENTS_RETRIEVAL_LIMIT = settings.DOCUMENTS_RETRIEVAL_LIMIT


retrieval_logger.warning(f"collection_name {collection_name}")
retrieval_logger.warning(f"DOCUMENTS_RETRIEVAL_LIMIT {DOCUMENTS_RETRIEVAL_LIMIT}")






def retrieval_node(state: BotState):
    retrieval_logger.info(f"[{state['conversation_id']}] ---RETRIEVE---")

    query = state["messages"][-1].content

    retrieval_logger.info(f"[{state['conversation_id']}] Rewritten Query: {query}")

    vector = embedding_function.embed_query(query)
    
    results = client.query_points(collection_name, query=vector, limit=DOCUMENTS_RETRIEVAL_LIMIT)
    # print(results)
    # context="context:\n"
    # context += "\n ".join([r.payload["information"] for r in results.points])
    
    retrieved_documents= [f"{r.payload}" for r in results.points]
    
    retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {len(retrieved_documents)} documents")
    retrieval_logger.info(f"[{state['conversation_id']}] {retrieved_documents}")
    return {"retrieved_documents": retrieved_documents}