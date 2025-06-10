from typing_extensions import TypedDict
from typing import List
from typing import Annotated, Literal
from langgraph.graph.message import add_messages
### State

class State(TypedDict):
    user_content: str
    bot_content: str
    
    messages: Annotated[list, add_messages]
    documents : List[str]
    
def default_state() -> State:
    return {
        "user_content":"",
        "bot_content":"",
        "messages": [],
        "documents": [],
    }
    