
# Load the .env file
from dotenv import load_dotenv
load_dotenv(override=True)

import logger_config

from bot.retrieval import generate_and_store_vector_embeddings

if __name__ == "__main__":
    generate_and_store_vector_embeddings()
