import telebot
import requests

# telegram bot
bot = telebot.TeleBot("") 

# Handles all sent documents and audio files
@bot.message_handler(content_types=['video_note'])
def video_processing(message):
    print('video')
    bot.send_message(message.chat.id, 'Fazendo upload do vídeo, aguarde...')
    file_info = bot.get_file(message.video_note.file_id)
    
    downloaded_file = bot.download_file(file_info.file_path)
    with open('new_file.mkv', 'wb') as new_file:
        new_file.write(downloaded_file)
    
    bot.send_message(message.chat.id, 'Vídeo recebido com sucesso!')  
    
bot.infinity_polling()