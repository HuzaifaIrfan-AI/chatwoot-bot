
# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio

from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

client = MultiServerMCPClient({
  "qdrant": {
    "url": "http://localhost:1234/sse",
    "transport": "sse"
  }
})

from langchain_core.tools import BaseTool
from langchain.schema import Document
# 
async def store_documents(documents: list[Document]):
    
    tools = await client.get_tools()  # ← fetches all tools from all connected MCP servers
    print(tools)
    
    tool = tools[0]  # or match by name
    print(tool.name)
    print(tool.description)
    # Show schema (input arguments)
    print(tool.args_schema)
    
    # content="Huzaifa lives in Lahore"
    for document in documents:    
        content={
            "information": document.page_content,
            "metadata":document.metadata
        }
        result = await tool.ainvoke(content)
        print(result)


import glob

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
DOC_PATH = "./data/*.md"
TOP_K=4

def get_store_documents():
    # Step 2: Load markdown files
    documents = []
    for path in glob.glob(DOC_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": path}))

    # Step 3: Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)
    
    print(split_docs)
    asyncio.run(store_documents(split_docs))

def main():
    get_store_documents()



if __name__ == "__main__":
    main()
