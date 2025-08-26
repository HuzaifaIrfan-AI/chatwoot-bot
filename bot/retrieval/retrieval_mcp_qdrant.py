
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
# from langchain.schema import SystemMessage, HumanMessage , AIMessage
import os

from bot.State import BotState


from logger import retrieval_logger

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import asyncio

client = MultiServerMCPClient({
  "qdrant": {
    "url": "http://localhost:1234/sse",
    "transport": "sse"
  }
})

from settings import settings

DOCUMENTS_RETRIEVAL_LIMIT = settings.DOCUMENTS_RETRIEVAL_LIMIT

async def get_available_tools():
    tools = await client.get_tools()  # Fetches all tools from all connected MCP servers
    print(tools)
    return tools

tools=asyncio.run(get_available_tools())
print(f"Available tools: {len(tools)}")



async def retrieve_documents(query:str):
    
    tool = tools[1]  # qdrant-find
    print(tool.name)
    print(tool.description)
    # Show schema (input arguments)
    print(tool.args_schema)
    
    results = await tool.ainvoke({
        "query": query
    })

    return results[1:DOCUMENTS_RETRIEVAL_LIMIT+1]



collection_name="mcp_middlehost"

def retrieval_node(state: BotState):
    retrieval_logger.info(f"[{state["conversation_id"]}] ---RETRIEVE---")
    
    query = state["messages"][-1].content

    retrieved_documents= asyncio.run(retrieve_documents(query))
    
    retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {len(retrieved_documents)} documents")
    # retrieval_logger.info(f"[{state['conversation_id']}] Retrieved {retrieved_documents}")
    return {"retrieved_documents": retrieved_documents}