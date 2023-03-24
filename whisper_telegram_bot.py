import os
os.system("pip install -U openai-whisper")
import telebot
import configparser
import whisper

# Load bot token from conf.ini file
config = configparser.ConfigParser()
config.read('conf.ini')
BOT_TOKEN=config['Telegram']['BOT_TOKEN']

# Load model
model = whisper.load_model("medium")

# Create bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# Handle /start and /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "This is a bot that uses the Whisper library to transcribe audio messages.")
        
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])		
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

# Handle all audio messages
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
	file_info = bot.get_file(message.audio.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open("audio.ogg", 'wb') as new_file:
		new_file.write(downloaded_file)
	audio = whisper.load_audio("audio.ogg")
	audio = whisper.pad_or_trim(audio)
	mel = whisper.log_mel_spectrogram(audio).to(model.device)
	_, probs = model.detect_language(mel)
	options = whisper.DecodingOptions(fp16 = False)
	result = whisper.decode(model, mel, options)
	bot.reply_to(message, result.text)

# Handle all voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
	file_info = bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open("voice.ogg", 'wb') as new_file:
		new_file.write(downloaded_file)
	audio = whisper.load_audio("voice.ogg")
	audio = whisper.pad_or_trim(audio)
	mel = whisper.log_mel_spectrogram(audio).to(model.device)
	_, probs = model.detect_language(mel)
	options = whisper.DecodingOptions(fp16 = False)
	result = whisper.decode(model, mel, options)
	bot.reply_to(message, result.text)

# Run bot
if __name__ == '__main__':
    bot.infinity_polling()
