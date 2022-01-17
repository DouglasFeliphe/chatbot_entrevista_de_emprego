import telebot
import requests

# telegram bot
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg") 

# Handles all sent documents and audio files
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    file_info = bot.get_file(message.voice.file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.ogg', 'wb') as new_file:
        new_file.write(downloaded_file)
      
    
bot.infinity_polling()