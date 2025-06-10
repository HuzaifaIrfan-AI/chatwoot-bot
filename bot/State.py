from typing_extensions import TypedDict
from typing import List
### State

class State(TypedDict):
    user_content: str
    bot_content: str
    
    conversation_id:str
    messages: List[str]
    documents : List[str]
    
    open_conversation_state: bool
    
    
def default_state() -> State:
    return {
        "user_content":"",
        "bot_content":"",
        
        "conversation_id":"1",
        "messages": [],
        "documents": [],
        
        "open_conversation_state": False
    }
    