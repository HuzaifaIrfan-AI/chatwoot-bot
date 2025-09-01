
import os
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.redis import RedisSaver
import redis


from logger import bot_logger

bot_logger.warning("---Bot Started---")


from bot.State import BotState
from bot.generation import generation_node
from bot.retrieval import retrieval_node

from settings import settings

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT
REDIS_PASS = settings.REDIS_PASS
# Connect to Redis with password (adjust accordingly)
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, db=0)
bot_logger.warning(f"REDIS_URL at '{REDIS_HOST}' Port'{REDIS_PORT}'")


# 1. Connect to Redis
redis_cache = RedisSaver(redis_client=redis_client)

redis_cache.setup()


# 4. Define a simple graph with one loop
builder = StateGraph(BotState)

builder.add_node("retrieval", retrieval_node)
builder.add_node("generation", generation_node)


# Graph structure
builder.set_entry_point("retrieval")
builder.add_edge("retrieval", "generation")
builder.add_edge("generation", END)

bot = builder.compile(checkpointer=redis_cache)




