import requests
import glob
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
DOC_PATH = "./data/*.md"
PERSIST_DIRECTORY="vector_store"
TOP_K=4
import os
import logging
retriever_logger=logging.getLogger("retriever")


# Access environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_EMBEDDINGS_MODEL = os.getenv("OPENAI_EMBEDDINGS_MODEL", "text-embedding-3-small")


retriever_logger.info(f"Using OpenAI Embedding'{OPENAI_EMBEDDINGS_MODEL}'")
from langchain_openai.embeddings import OpenAIEmbeddings
embedding_function = OpenAIEmbeddings(model = OPENAI_EMBEDDINGS_MODEL,api_key=OPENAI_API_KEY)
PERSIST_DIRECTORY=PERSIST_DIRECTORY+"_"+OPENAI_EMBEDDINGS_MODEL

vectordb = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embedding_function)
retriever = vectordb.as_retriever(search_kwargs={"k":TOP_K})


def generate_and_store_vector_embeddings():
    
    # Step 2: Load markdown files
    documents = []
    for path in glob.glob(DOC_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": path}))

    # Step 3: Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding_function,
        persist_directory=PERSIST_DIRECTORY
    )
    

    retriever_logger.info(f"✅ vector store created and saved to '{PERSIST_DIRECTORY}'")
    
    
import json

from bot import State
def retrieve(state: State):
    retriever_logger.info(f"[{state["conversation_id"]}] ---RETRIEVE---")
    
    user_content = state["user_content"]

    # Retrieval
    retrieved_documents = retriever.invoke(user_content)
    
    # retriever_logger.info(f"{retrieved_documents}") 
    
    for document in retrieved_documents:
        state["documents"].append(document.page_content)
    
    # state["documents"].extend(documents)
    
    # retriever_logger.info(f"{state["documents"]}") 
    
    return 
    # return {"documents": state["documents"]}