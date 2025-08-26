from typing import Annotated, TypedDict
from langgraph.graph import MessagesState, add_messages
from langchain_core.messages import AnyMessage
from typing import List

import os

from settings import settings

MAX_MESSAGES_CACHED = settings.MAX_MESSAGES_CACHED
MAX_DOCUMENTS_CACHED = settings.MAX_DOCUMENTS_CACHED

def add_and_trim_messages(prev: list[AnyMessage], new: list[AnyMessage]) -> list[AnyMessage]:
    combined = (prev or []) + new
    return combined[-MAX_MESSAGES_CACHED:]


def add_and_trim_documents(prev: list[str], new: list[str]) -> list[str]:
    combined = (prev or []) + new
    return combined[-MAX_DOCUMENTS_CACHED:]

# Define shared state
class BotState(TypedDict): 
    conversation_id: str  
    retrieved_documents : Annotated[list[AnyMessage], add_and_trim_documents]
    messages: Annotated[list[AnyMessage], add_and_trim_messages]

    

    open_conversation_state: bool