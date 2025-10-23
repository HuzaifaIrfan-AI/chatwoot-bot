


from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState

# Access environment variables
from settings import settings



# from bot.retrieval.retrieval_mcp_qdrant import retrieval_node
from bot.retrieval.retrieval_qdrant import retrieval_node


from logger import retrieval_logger

SYSTEM_CONTENT = """
You are a helpful query rewriter for a RAG system.
Rewrite the latest user query for more effective document retrieval.

Use the previous AI messages as context.

if you do not know the context, word or acronym, do not rewrite the query.

If the current query is not related to the previous conversation,
respond with the query itself without rewriting it.

Respond only with a rewritten, retrieval-friendly version of the query.
"""

SYSTEM_MESSAGE=SystemMessage(SYSTEM_CONTENT)

USE_API = settings.USE_API






if USE_API == "ollama":
    # Initialize your query_rewriter model
    from langchain_ollama import ChatOllama

    OLLAMA_API_URL = settings.OLLAMA_API_URL
    OLLAMA_REWRITER_MODEL = settings.OLLAMA_REWRITER_MODEL

    query_rewriter_llm = ChatOllama(
        base_url=OLLAMA_API_URL,
        model=OLLAMA_REWRITER_MODEL
    )

    REWRITER_MODEL=OLLAMA_REWRITER_MODEL


elif USE_API == "google":
    # Initialize your query_rewriter model
    from langchain_google_genai import ChatGoogleGenerativeAI

    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    GOOGLE_REWRITER_MODEL = settings.GOOGLE_REWRITER_MODEL

    query_rewriter_llm = ChatGoogleGenerativeAI(
        model=GOOGLE_REWRITER_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,         # optional, same as OpenAI temperature
    )

    REWRITER_MODEL=GOOGLE_REWRITER_MODEL



else:
# if USE_API == "openai":
    # Initialize your query_rewriter model
    from langchain_openai import ChatOpenAI
    OPENAI_API_KEY = settings.OPENAI_API_KEY
    OPENAI_REWRITER_MODEL = settings.OPENAI_REWRITER_MODEL
    query_rewriter_llm = ChatOpenAI(model=OPENAI_REWRITER_MODEL, api_key=OPENAI_API_KEY)

    REWRITER_MODEL=OPENAI_REWRITER_MODEL



retrieval_logger.warning(f"Using rewriter Model'{REWRITER_MODEL}'")


# temperature=0.0
def query_rewriter_node(state: BotState):
    retrieval_logger.info(f"[{state['conversation_id']}] ---QueryRewriter---")

    user_messages = [msg.content for msg in state["messages"] if isinstance(msg, HumanMessage)][-3:-2]

    last_ai_message = state["messages"][-2].content if len(state["messages"]) > 1 else None

    user_query = state["messages"][-1].content

    # Build the rewriting prompt
    # Previous User Messages:
    # {chr(10).join(user_messages) or "None"}
    # ---
    prompt = f"""
    Last AI Message:
    {last_ai_message or "None"}
    ---
    Current User Query:
    {user_query}
    """

    retrieval_logger.info(f"[{state['conversation_id']}] Query Rewriter Prompt: {prompt}")

    rewritten_response = query_rewriter_llm.invoke([SYSTEM_MESSAGE, HumanMessage(prompt)])

    state["messages"][-1].content = rewritten_response.content

    return state