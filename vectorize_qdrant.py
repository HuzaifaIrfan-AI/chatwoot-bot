
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`
import os

from settings import settings
QDRANT_URL = settings.QDRANT_URL

client = QdrantClient(QDRANT_URL)

collection_name="middlehost"

if not client.collection_exists(collection_name=collection_name):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )


from langchain_core.tools import BaseTool
from langchain.schema import Document
# 

# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai.embeddings import OpenAIEmbeddings

import os
# Access environment variables
OPENAI_API_KEY = settings.OPENAI_API_KEY
OPENAI_EMBEDDINGS_MODEL = settings.OPENAI_EMBEDDINGS_MODEL

embeddings_function=OpenAIEmbeddings(model = OPENAI_EMBEDDINGS_MODEL,api_key=OPENAI_API_KEY)


def store_documents(documents: list[Document]):
    
    page_contents = [document.page_content for document in documents]

    vectors=embeddings_function.embed_documents(page_contents)
    
    for i, (document, vector) in enumerate(zip(documents, vectors)):
    # print(vectors)
        payload={
            "information": document.page_content,
            "metadata":document.metadata
        }
        
        client.upload_collection(
            collection_name=collection_name,
            vectors=[vector],
            payload=[payload]
        )
        print(f"Document {i+1} stored with metadata: {document.metadata}")


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
    store_documents(split_docs)

def main():
    get_store_documents()



if __name__ == "__main__":
    main()
