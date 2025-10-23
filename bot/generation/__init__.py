



# 3. Define a simple chat node using OpenAI

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

from settings import settings



USE_API = settings.USE_API





if USE_API == "ollama":
    # Initialize your query_rewriter model
    from langchain_ollama import ChatOllama

    OLLAMA_API_URL = settings.OLLAMA_API_URL
    OLLAMA_MODEL = settings.OLLAMA_MODEL

    llm = ChatOllama(
        base_url=OLLAMA_API_URL,
        model=OLLAMA_MODEL
    )

    GEN_MODEL=OLLAMA_MODEL

elif USE_API == "google":
    # Initialize your query_rewriter model
    from langchain_google_genai import ChatGoogleGenerativeAI

    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    GOOGLE_MODEL = settings.GOOGLE_MODEL

    llm = ChatGoogleGenerativeAI(
        model=GOOGLE_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.5,         # optional, same as OpenAI temperature
    )

    GEN_MODEL=GOOGLE_MODEL



else:
# if USE_API == "openai":
    # Initialize your query_rewriter model
    from langchain_openai import ChatOpenAI
    OPENAI_API_KEY = settings.OPENAI_API_KEY
    OPENAI_MODEL = settings.OPENAI_MODEL
    llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY)

    GEN_MODEL=OPENAI_MODEL






from config import SYSTEM_CONTENT


SYSTEM_MESSAGE=SystemMessage(SYSTEM_CONTENT)

from logger import generation_logger

# generation_logger.info(f"SYSTEM_CONTENT: '''{SYSTEM_CONTENT}'''")

generation_logger.warning(f"Using gen Model'{GEN_MODEL}'")


def generation_node(state: BotState) -> BotState:
    
    generation_logger.info(f"[{state["conversation_id"]}] ---GENERATE---")
    retrieved_documents = state.get("retrieved_documents", [])
    
    retrieved_documents_context="retrieved_documents_context:\n"
    retrieved_documents_context += "\n ".join(retrieved_documents)
    retrieved_documents_message = SystemMessage(content=retrieved_documents_context)
    
    messages = state.get("messages", [])
    response = llm.invoke([SYSTEM_MESSAGE]+messages+[retrieved_documents_message])  

    generation_logger.info(f"[{state["conversation_id"]}] {response.content}")
    
    return {"messages": [response]}
