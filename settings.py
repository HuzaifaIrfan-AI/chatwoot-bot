


from pydantic import Field

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    KAFKA_URL: str = Field(default="kafka:9092", alias="KAFKA_URL")

    USE_API: str = Field(default="openai", alias="USE_API")
    USE_EMBEDDINGS_API: str = Field(default="openai", alias="USE_EMBEDDINGS_API")

    OLLAMA_API_URL: str = Field(default="http://localhost:11434", alias="OLLAMA_API_URL")
    OLLAMA_MODEL: str = Field(default="llama3.2", alias="OLLAMA_MODEL")
    OLLAMA_REWRITER_MODEL: str = Field(default="llama3.2", alias="OLLAMA_REWRITER_MODEL")
    OLLAMA_EMBEDDINGS_MODEL: str = Field(default="nomic-embed-text", alias="OLLAMA_EMBEDDINGS_MODEL")

    GOOGLE_API_KEY: str = Field(default="", alias="GOOGLE_API_KEY")
    GOOGLE_MODEL: str = Field(default="models/gemini-2.5-flash-lite", alias="GOOGLE_MODEL")
    GOOGLE_REWRITER_MODEL: str = Field(default="models/gemini-2.5-flash-lite", alias="GOOGLE_REWRITER_MODEL")
    GOOGLE_EMBEDDINGS_MODEL: str = Field(default="gemini-embedding-001", alias="GOOGLE_EMBEDDINGS_MODEL")

    OPENAI_API_KEY: str = Field(default="sk-proj-", alias="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-5-mini", alias="OPENAI_MODEL")
    OPENAI_REWRITER_MODEL: str = Field(default="gpt-5-mini", alias="OPENAI_REWRITER_MODEL")
    OPENAI_EMBEDDINGS_MODEL: str = Field(default="text-embedding-3-small", alias="OPENAI_EMBEDDINGS_MODEL")

    REDIS_HOST: str = Field(default="redis", alias="REDIS_HOST")
    REDIS_PORT: str = Field(default="6379", alias="REDIS_PORT")
    REDIS_PASS: str = Field(default="aa", alias="REDIS_PASS")


    QDRANT_URL: str = Field(default="http://qdrant:6333", alias="QDRANT_URL")
    COLLECTION_NAME: str = Field(default="rag_bot", alias="COLLECTION_NAME")

    MAX_MESSAGES_CACHED: int = Field(default=50, alias="MAX_MESSAGES_CACHED")
    MAX_DOCUMENTS_CACHED: int = Field(default=6, alias="MAX_DOCUMENTS_CACHED")
    DOCUMENTS_RETRIEVAL_LIMIT: int = Field(default=3, alias="DOCUMENTS_RETRIEVAL_LIMIT")

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        populate_by_name=True 
    )



settings = Settings()
