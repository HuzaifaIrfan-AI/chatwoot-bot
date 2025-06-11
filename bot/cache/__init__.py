import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from State import State, default_state

import logging

bot_logger=logging.getLogger("bot")


messages_cache={
    
}

documents_cache={
    
}



def get_cache(state: State):
    bot_logger.info(f"{state["conversation_id"]}---Cache Get---")
    
    conversation_id=state["conversation_id"]
    
    
    messages = messages_cache.get(conversation_id, [])[-100:]
    
    documents = documents_cache.get(conversation_id, [])[-4:]
    
    # print(messages_cache) 
    
    return {"messages": messages, "documents": documents}





def update_cache(state: State):
    bot_logger.info(f"{state["conversation_id"]}---Cache Update---")
    
    conversation_id=state["conversation_id"]
    user_content=state["user_content"]
    bot_content=state["bot_content"]
    
    if not messages_cache.get(conversation_id, []):
        messages_cache[conversation_id]=[]

    
    user_message={"role": "user",
         "content": user_content
    }
    
    bot_message={"role": "assistant",
         "content": bot_content
    }
    
    messages_cache[conversation_id].append(user_message)
    messages_cache[conversation_id].append(bot_message)
    
    documents_cache[conversation_id]=state["documents"]

    return


if __name__=="__main__":
    
    state = default_state()
    state["conversation_id"] = "1"
    
    get_cache(state)
    update_cache(state)
    get_cache(state)