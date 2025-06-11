


from bot.State import State,default_state

import logging

bot_logger=logging.getLogger("bot")


import json

import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PASS = os.getenv("REDIS_PASS", "aa")
# Connect to Redis with password (adjust accordingly)
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, db=0)
bot_logger.warning(f"REDIS_URL at '{REDIS_HOST}' Port'{REDIS_PORT}'")



def get_cache(state: State):
    bot_logger.info(f"[{state["conversation_id"]}] ---Redis Cache Get---")
    
    conversation_id=state["conversation_id"]
    
    messages_cache_key = f'messages_cache::{conversation_id}'
    documents_cache_key = f'documents_cache::{conversation_id}'
   
    messages_dump = redis_client.lrange(messages_cache_key, -50, -1)
    messages = [json.loads(message_dump.decode('utf-8'))
                         for message_dump in messages_dump]
    
    documents_dump = redis_client.lrange(documents_cache_key, -4, -1)

    documents = [json.loads(document_dump.decode('utf-8'))
                         for document_dump in documents_dump]

    return {"messages": messages, "documents": documents}
    

def update_cache(state: State):
    bot_logger.info(f"[{state["conversation_id"]}] ---Redis Cache Update---")
    
    conversation_id=state["conversation_id"]
    user_content=state["user_content"]
    bot_content=state["bot_content"]
    messages_cache_key = f'messages_cache::{conversation_id}'
    documents_cache_key = f'documents_cache::{conversation_id}'
    
    documents=state["documents"]
    
    user_message={"role": "user",
         "content": user_content
    }
    
    bot_message={"role": "assistant",
         "content": bot_content
    }
    
    # bot_logger.info(f"{state["documents"]}")
    # bot_logger.info(f"{state["messages"]}")
    
    redis_client.rpush(messages_cache_key, json.dumps(user_message))
    redis_client.rpush(messages_cache_key, json.dumps(bot_message))
    
    for document in documents:
        redis_client.rpush(documents_cache_key, json.dumps(document))
    
    # redis cleanup
    redis_client.ltrim(documents_cache_key, -4, -1)
   