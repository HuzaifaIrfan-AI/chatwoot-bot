



# 3. Define a simple chat node using OpenAI

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

from settings import settings
OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_MODEL = settings.OPENAI_MODEL

llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=0.1,
    openai_api_key=OPENAI_API_KEY
)



from config import SYSTEM_CONTENT


SYSTEM_MESSAGE=SystemMessage(SYSTEM_CONTENT)

from logger import generation_logger

# generation_logger.info(f"SYSTEM_CONTENT: '''{SYSTEM_CONTENT}'''")

generation_logger.info(f"Using OpenAI Model'{OPENAI_MODEL}'")


def generation_node(state: BotState) -> BotState:
    
    generation_logger.info(f"[{state["conversation_id"]}] ---GENERATE---")
    retrieved_documents = state.get("retrieved_documents", [])
    
    retrieved_documents_context="retrieved_documents_context:\n"
    retrieved_documents_context += "\n ".join(retrieved_documents)
    retrieved_documents_message = SystemMessage(content=retrieved_documents_context)
    
    messages = state.get("messages", [])
    response = llm.invoke([SYSTEM_MESSAGE]+messages+[retrieved_documents_message])  
    
    return {"messages": [response]}
