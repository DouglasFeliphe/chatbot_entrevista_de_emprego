import telebot

CHAVE_API = '2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg'

bot = telebot.TeleBot(CHAVE_API)

def verificar(mensagem):
  return True

@bot.message_handler(func=verificar)
def responder(mensagem):
  bot.reply_to(mensagem, "Olá, aqui é o bot de entrevista")

bot.polling()