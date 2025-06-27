# piv-bot

Telegram bot that analyses a shelf photo with beers and gives a recommendation using Ollama.

## Usage

1. Create a `.env` file with your Telegram `API_TOKEN`:
   ```
   API_TOKEN=YOUR_TELEGRAM_TOKEN
   OLLAMA_URL=http://ollama:11434/api/generate
   ```

2. Build and run services with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The bot will be available immediately and will communicate with the Ollama service running in the same compose network.

