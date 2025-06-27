# piv-bot

Telegram bot that analyses a shelf photo with beers and gives a recommendation using Ollama.

## Usage

1. Create a `.env` file with your Telegram `API_TOKEN` (optionally override the Ollama URL):
   ```
   API_TOKEN=YOUR_TELEGRAM_TOKEN
   OLLAMA_URL=http://localhost:11434/api/generate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start Ollama and download the required model:
   ```bash
   ollama serve &
   ollama pull mistral:7b
   ```

4. Run the bot:
   ```bash
   python main.py
   ```

The bot will be available immediately and communicate with the local Ollama service.
