
docker compose up --build -d
docker compose exec chatwoot_bot uv run cleanup_qdrant.py
docker compose exec chatwoot_bot uv run vectorize_qdrant.py
