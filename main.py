import telebot
from telebot import types
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  

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
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  itembtn1 = types.KeyboardButton('Sim')
  itembtn2 = types.KeyboardButton('Não')  
  markup.add(itembtn1, itembtn2)  
  msg = bot.send_message(message.chat.id, f'Ótimo! Anotei seu email como {email}. Está correto?', reply_markup=markup)

  if(message.text == "Sim"):
    bot.register_next_step_handler(msg, get_password)
  else:
    bot.register_next_step_handler(msg, send_welcome)


@bot.message_handler(func=lambda message: True)
def get_password(message):
  bot.send_message(message.chat.id, f'Agora, informe uma senha de acesso (fique tranquilo nossas mensagens são criptografadas)')
  password = message.text   


bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

print('bot rodando')

bot.infinity_polling()  
