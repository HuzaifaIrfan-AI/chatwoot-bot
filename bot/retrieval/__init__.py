

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

# Access environment variables
from settings import settings

OPENAI_API_KEY = settings.OPENAI_API_KEY

# from bot.retrieval.retrieval_mcp_qdrant import retrieval_node
from bot.retrieval.retrieval_qdrant import retrieval_node


from logger import retrieval_logger



# Initialize your query_rewriter model
query_rewriter_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

def query_rewriter_node(state: BotState):
    retrieval_logger.info(f"[{state['conversation_id']}] ---QueryRewriter---")

    user_messages = [msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)][-5:]

    last_ai_message = state["messages"][-2].content if len(state["messages"]) > 1 else None

    user_query = state["messages"][-1].content

    # Build the rewriting prompt
    prompt = f"""
    You are a helpful query rewriter for a RAG system.
    Rewrite the latest user query for more effective document retrieval.

    Use the previous 5 user messages and the last AI message as context.

    ---
    Previous User Messages:
    {chr(10).join(user_messages) or "None"}
    ---
    Last AI Message:
    {last_ai_message or "None"}
    ---
    Current User Query:
    {user_query}
    ---

    Respond only with a rewritten, retrieval-friendly version of the query.
    """

    retrieval_logger.info(f"[{state['conversation_id']}] Query Rewriter Prompt: {prompt}")

    rewritten_response = query_rewriter_llm.invoke([HumanMessage(prompt)])

    state["messages"][-1].content = rewritten_response.content

    return state