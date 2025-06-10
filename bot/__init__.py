

import json

from chatwoot import create_new_message, open_conversation_status


from bot.cache import update_cache,get_cache
from bot.generation import generate

from langgraph.graph import StateGraph, START, END


from bot.State import State, default_state


graph_builder = StateGraph(State)

graph_builder.add_node("get_cache", get_cache)
graph_builder.add_node("update_cache", update_cache)

graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "get_cache")
graph_builder.add_edge("get_cache", "generate")
graph_builder.add_edge("generate", "update_cache")
graph_builder.add_edge("update_cache", END)
bot = graph_builder.compile()

import logging


bot_logger=logging.getLogger("bot")
bot_logger.warning("bot Started")


CONVERSATION_OPENED_CONTENT="Your chat is transferred to human. Please wait."

def process_pending_user_messages(payload):
    account_id=payload["account_id"]
    conversation_id=payload["conversation_id"]
    name=payload["name"]
    email=payload["email"]
    phonenumber=payload["phonenumber"]
    content=payload["content"]
    
    # bot_content=f"{name}: {content}"
    
    state = default_state()
    state["conversation_id"] = str(conversation_id)
    state["user_content"] = content
    state = bot.invoke(state)
    
    open_conversation_state=state["open_conversation_state"]
    bot_content=state["bot_content"]
    
    if (open_conversation_state):
        open_conversation_status(account_id, conversation_id)
        bot_content=CONVERSATION_OPENED_CONTENT
    
    create_new_message(account_id, conversation_id, bot_content)
    
    return bot_content

