
import telebot

bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg")

firstTime = True

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):  
	bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, "Ola este é o BOT. Informe seu email por favor: ")

  if message=='teste@teste.com'
  # firstTime = False

@bot.message_handler(func=lambda message: True)
def function_name(message):
  if re.search(r'@|.', message.text) and not firstTime:
	  bot.reply_to(message, "This is a message handler")


print("Bot rodando...")

bot.infinity_polling()
