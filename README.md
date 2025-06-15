# chatwoot-bot

## Create .env
```sh
cp .env.example .env
```
- Add OPENAI_API_KEY in .env


## Create Vector Embeddings
```sh
sh vectorize.sh
```

## Run Docker
```sh
docker compose up --build
```