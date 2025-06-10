

import json

from chatwoot import create_new_message, open_conversation_status



from bot.generation import generate

from langgraph.graph import StateGraph, START, END


from bot.State import State, default_state


graph_builder = StateGraph(State)

graph_builder.add_node("generate", generate)
graph_builder.add_edge(START, "generate")
graph_builder.add_edge("generate", END)
bot = graph_builder.compile()

import logging


bot_logger=logging.getLogger("bot")
bot_logger.warning("bot Started")




def process_pending_user_messages(payload):
    account_id=payload["account_id"]
    conversation_id=payload["conversation_id"]
    name=payload["name"]
    email=payload["email"]
    phonenumber=payload["phonenumber"]
    content=payload["content"]
    
    # bot_content=f"{name}: {content}"
    
    state = default_state()
    state["user_content"] = content
    state = bot.invoke(state)
    bot_content=state["bot_content"]
    
    create_new_message(account_id, conversation_id, bot_content)
    
    return bot_content

