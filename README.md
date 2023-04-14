# Telegram Audio Transcription Bot

This is a Telegram bot that uses the Whisper library to transcribe audio messages. It can transcribe both audio and voice messages in multiple languages.

## Installation

To use this bot, you need to have Python 3.x installed on your machine. You also need to install the `openai-whisper` library:

```bash
pip install -U openai-whisper
```

## Usage

1. Clone the repository and navigate to the root folder.
2. Create a new file called `conf.ini` and add the following content:

   ```ini
   [Telegram]
   BOT_TOKEN=<your-bot-token>
   ```

   Replace `<your-bot-token>` with your Telegram bot token.
3. Start the bot by running the following command:

   ```bash
   python whisper_telegram_bot.py
   ```

   The bot will start listening for incoming messages.
4. Send an audio or voice message to the bot, and it will transcribe the message and send the result back to you.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project uses the following open source libraries:

- [OpenAI Whisper](https://github.com/openai/whisper): for speech recognition and language detection.
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): for building the Telegram bot.