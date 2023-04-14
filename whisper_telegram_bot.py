import os
# os.system("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118")
# os.system("pip install -U openai-whisper")
# os.system("pip install -U pyTelegramBotAPI")
import telebot
from telebot import types
import configparser
import whisper
import datetime

# Load bot token from conf.ini file
config = configparser.ConfigParser()
config.read('conf.ini')
BOT_TOKEN=config['Telegram']['BOT_TOKEN']

# Load model
model = whisper.load_model("small")

# Create bot
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

# Create bot commands
bot.set_my_commands([{'command': 'start', 'description': 'Start the bot'}, {'command': 'help', 'description': 'Help'}])

# Define the menu options
menu_options = ['English', 'Spanish', 'French', 'German', 'Italian', 'Portuguese', 'Russian', 'Japanese', 'Korean', 'Chinese']

# Define the function that will handle the menu request
def handle_menu(callback_query):
	# Get the message from the callback query
	message = callback_query.message
	# Get the user from the callback query
	user = callback_query.from_user
	# Get the data from the callback query
	data = callback_query.data
	# Get the message id from the callback query
	message_id = message.message_id
	# Get the chat id from the callback query
	chat_id = message.chat.id
	# Get the message text from the callback query
	message_text = message.text
	# Get the message date from the callback query
	message_date = message.date
	bot.answer_callback_query(callback_query.id, text=f"You {user} have selected {data}")

# Add the callback query handler for the menu options
bot.callback_query_handler(func=handle_menu)	

# Handle /menu command
@bot.message_handler(commands=['menu'])
def send_menu(message):
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
	markup.add(*menu_options)
	bot.reply_to(message, "Select a language:", reply_markup=markup)

# Handle /start and /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "This is a bot that uses the Whisper AI model to transcribe audio messages.\n"+
						"You can send an audio file or a voice message to the bot and it will transcribe it.\n"+
						"Note that the bot is still in development and may not work properly.\n"+
						"Voice messages are transcribed faster than audio files. But with 30 seconds length limit.")
        
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])		
@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)

# Handle all audio messages
@bot.message_handler(content_types=['audio'])
def handle_audio(message):
	file_info = bot.get_file(message.audio.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open(f"{message.message_id}_audio.ogg", 'wb') as new_file:
		new_file.write(downloaded_file)
	# Log current time	
	print(f"Transcribing audio from message {message.message_id} start time {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	# Transcribe audio with model.transcribe() which has no length limit
	result = model.transcribe(f"{message.message_id}_audio.ogg", fp16=False)
	print(f"Transcribing audio from message {message.message_id} finish time {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	bot.reply_to(message, result["text"])

# Handle all voice messages
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
	file_info = bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open(f"{message.message_id}_voice.ogg", 'wb') as new_file:
		new_file.write(downloaded_file)
	print(f"Transcribing voice from message {message.message_id} start time {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	audio = whisper.load_audio(f"{message.message_id}_voice.ogg")
	audio = whisper.pad_or_trim(audio)
	mel = whisper.log_mel_spectrogram(audio).to(model.device)
	_, probs = model.detect_language(mel)
	print(f"Detected language: {max(probs, key=probs.get)}")
	options = whisper.DecodingOptions(fp16 = False)
	result = whisper.decode(model, mel, options)
	print(f"Transcribing voice from message {message.message_id} finish time {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
	bot.reply_to(message, result.text)

# Run bot
if __name__ == '__main__':
    bot.infinity_polling()
