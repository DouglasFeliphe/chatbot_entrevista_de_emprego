import telebot

username = ''
email = ''

bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Ola este é o BOT. Informe seu email por favor?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)    

@bot.message_handler(regexp="SOME_REGEXP")
def handle_message(message):  
		bot.reply_to(message, "regex?")  

@bot.message_handler(commands=['hello'])
def send_hello(message):
	bot.reply_to(message, "Howdy, how are you doing?")    

print('bot rodando')

bot.infinity_polling()  
