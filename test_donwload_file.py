import telebot
import requests

# telegram bot
bot = telebot.TeleBot("") 

@bot.message_handler(content_types=['document'])    
def handle_document(message):
    filename = message.document.file_name    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'File downloaded')  
     
      
    
bot.infinity_polling()