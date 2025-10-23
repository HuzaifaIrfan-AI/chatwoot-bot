
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# client = QdrantClient(":memory:")  # Or use `host="localhost", port=6333`
import os

from settings import settings
QDRANT_URL = settings.QDRANT_URL
USE_EMBEDDINGS_API = settings.USE_EMBEDDINGS_API

client = QdrantClient(QDRANT_URL)

COLLECTION_NAME_PREFIX=settings.COLLECTION_NAME


from langchain_core.tools import BaseTool
from langchain.schema import Document
# 




if USE_EMBEDDINGS_API == "ollama":

    from langchain_ollama import OllamaEmbeddings

    OLLAMA_EMBEDDINGS_MODEL = settings.OLLAMA_EMBEDDINGS_MODEL
    OLLAMA_API_URL = settings.OLLAMA_API_URL

    embedding_function = OllamaEmbeddings(
        base_url=OLLAMA_API_URL,
        model=OLLAMA_EMBEDDINGS_MODEL
    )

    collection_name=f"{COLLECTION_NAME_PREFIX}_{OLLAMA_EMBEDDINGS_MODEL}"

elif USE_EMBEDDINGS_API == "google":

    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    GOOGLE_API_KEY = settings.GOOGLE_API_KEY
    GOOGLE_EMBEDDINGS_MODEL = settings.GOOGLE_EMBEDDINGS_MODEL

    embedding_function = GoogleGenerativeAIEmbeddings(
        model=GOOGLE_EMBEDDINGS_MODEL,  # Gemini embedding model
        google_api_key=GOOGLE_API_KEY
    )

    collection_name=f"{COLLECTION_NAME_PREFIX}_{GOOGLE_EMBEDDINGS_MODEL}"


else:

# if USE_EMBEDDINGS_API == "openai":

    from langchain_openai.embeddings import OpenAIEmbeddings

    # Access environment variables
    OPENAI_API_KEY = settings.OPENAI_API_KEY
    OPENAI_EMBEDDINGS_MODEL = settings.OPENAI_EMBEDDINGS_MODEL

    embedding_function=OpenAIEmbeddings(model = OPENAI_EMBEDDINGS_MODEL,api_key=OPENAI_API_KEY)
    collection_name=f"{COLLECTION_NAME_PREFIX}_{OPENAI_EMBEDDINGS_MODEL}"





from langchain_qdrant import QdrantVectorStore

qdrant = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
    embedding=embedding_function,
)


def cleanup_db():

    if client.collection_exists(collection_name=collection_name):
        client.delete_collection(collection_name=collection_name)
        print(f"'{collection_name}' collection deleted")
    else:
        print(f"'{collection_name}' collection not exist")


    # --- 3️⃣ Ensure Collection Exists ---
    # You must specify vector size and distance manually
    vector_size = len(embedding_function.embed_query("test"))  # auto-detect dimension

    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        ),
    )




import glob

from langchain.text_splitter import RecursiveCharacterTextSplitter

# Constants
DOC_PATH = "./data/*.md"
TOP_K=4

import time

def get_store_documents():
    # Step 2: Load markdown files
    documents = []
    for path in glob.glob(DOC_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(Document(page_content=content, metadata={"source": path}))

    # Step 3: Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=300)
    split_docs = splitter.split_documents(documents)
    
    print(split_docs)


    cleanup_db()

    # --- 6️⃣ Store in Qdrant ---
    # qdrant.add_documents(split_docs)


    print(f"\n🧩 Prepared {len(split_docs)} chunks. Starting upload...\n")

    # --- 5️⃣ Verbose Store ---
    start_time = time.time()
    for i, doc in enumerate(split_docs, start=1):
        print(f"📄 [{i}/{len(split_docs)}] Embedding & storing chunk ({len(doc.page_content)} chars)...", end="")
        start = time.time()
        qdrant.add_documents([doc])  # add one by one for progress visibility
        end = time.time()
        print(f" ✅ done in {end - start:.2f}s | Metadata: {doc.metadata}")
    end_time = time.time()

    # --- 6️⃣ Confirm Final Count ---
    count = qdrant.client.count(qdrant.collection_name).count
    print(f"\n📊 Done! Total vectors in collection '{collection_name}': {count} in {end_time - start_time:.2f}s")


def main():
    get_store_documents()
    print(f"Documents have been stored in collection {collection_name} in Qdrant {settings.QDRANT_URL}")



if __name__ == "__main__":
    main()

