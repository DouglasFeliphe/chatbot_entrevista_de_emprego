import telebot
from telebot import types

username = ''
confirmEmail = False
email = ''
password = ''

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg") 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  username = message.from_user.first_name  
  bot.send_message(message.chat.id, f"Ola @{username} este é o ENTREVIBOT. Informe seu email por favor?")  

@bot.message_handler(func=lambda message: True)
def get_email(message):
  email = message.text
  markup = types.ReplyKeyboardMarkup(row_width=2)
  itembtn1 = types.KeyboardButton('Sim')
  itembtn2 = types.KeyboardButton('Não')  
  markup.add(itembtn1, itembtn2)  
  bot.send_message(message.chat.id, f'Ótimo! Anotei seu email como {email}. Está correto?', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def confirm_email(message):  
  bot.send_message(message.chat.id, f'Agora, informe uma senha de acesso (fique tranquilo nossas mensagens são criptografadas)', reply_markup=markup)  

# @bot.message_handler(func=lambda message: True)
# def get_password(message): 
#   bot.send_message(message.chat.id, f' Agora, informe uma senha de acesso (fique tranquilo nossas mensagens são criptografadas)')
#   password = message.text
#   markup = types.ReplyKeyboardMarkup(row_width=2)
#   itembtn1 = types.KeyboardButton('Sim')
#   itembtn2 = types.KeyboardButton('Não')  
#   markup.add(itembtn1, itembtn2) 
#   bot.send_message(message.chat.id, f'Ótimo! Anotei seu email como {email}. Está correto?', reply_markup=markup)






print('bot rodando')

bot.infinity_polling()  
