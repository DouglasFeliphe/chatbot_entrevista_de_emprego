import telebot

# telegram bot
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg") 

# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Olá")    
    print(message.document)
    
@bot.message_handler(content_types=['document'])    
def handle_document(message):
    print(message.document)

bot.infinity_polling()