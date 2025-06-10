import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from State import State, default_state


messages_cache={
    
}

def get_cache(state: State):
    conversation_id=state["conversation_id"]
    
    messages=[]
    
    if messages_cache.get(conversation_id):
        # print(messages_cache.get(conversation_id))
        for message in messages_cache.get(conversation_id)[-100:]:
            messages.append(message)
    else:
        pass
        # print(f"no messages_cache {conversation_id}")
    
    
    return {"messages": messages}





def update_cache(state: State):
    conversation_id=state["conversation_id"]
    user_content=state["user_content"]
    bot_content=state["bot_content"]
    
    if messages_cache.get(conversation_id):
        pass
        # print(messages_cache.get(conversation_id))
    else:
        # print(f"no messages_cache {conversation_id}")
        messages_cache[conversation_id]=[]
    
    user_message={"role": "user",
         "content": user_content
    }
    
    bot_message={"role": "assistant",
         "content": bot_content
    }
    
    messages_cache[conversation_id].append(user_message)
    messages_cache[conversation_id].append(bot_message)
    
    return


if __name__=="__main__":
    
    state = default_state()
    state["conversation_id"] = "1"

    
    get_cache(state)
    update_cache(state)
    get_cache(state)