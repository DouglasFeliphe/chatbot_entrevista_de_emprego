import telebot

username = ''
confirmEmail = False
email = ''

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg", parse_mode=None) 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  username = message.from_user.first_name  
  bot.reply_to(message, f"Ola @{username} este é o ENTREVIBOT. Informe seu email por favor?")  

@bot.message_handler(func=lambda message: True)
def get_email(message):
  email = message.text
  bot.reply_to(message, f'Ótimo! Anotei seu email como {email}. Está correto? \n/sim\n/nao')


print('bot rodando')

bot.infinity_polling()  
