from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
# from markup import getMarkup


# telegram bot
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg") 

# TODO:
# persist user data
# theme color for bot messages (blue, green, red, etc) 

user_dict = {}


class User:
    def __init__(self, fullname):
        self.fullname = fullname
        self.age = None
        self.sex = None
        
confirmFullname = False
confirmEmail = False        


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Ola, Eu sou o EntrevBot.
Informe seu nome completo:
""")
    bot.register_next_step_handler(msg, process_fullname_step)


def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        fullname = message.text
        user = User(fullname)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Informe seu email:')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')


def process_email_step(message):
    try:
        chat_id = message.chat.id
        email = message.text
        if email.isdigit():
            msg = bot.reply_to(message, 'O email que voce digitou é inválido. Informe um email válido:')
            bot.register_next_step_handler(msg, process_email_step)
            return
        user = user_dict[chat_id]
        user.email = email
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            resize_keyboard=True
            )       
        markup.add("Sim","Não")
        msg = bot.reply_to(message, f'Seu email é {user.email}.', reply_markup=markup)
        bot.register_next_step_handler(msg, process_confirm_email)        
            
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_confirm_email(message):
    msg = bot.send_message(message.chat.id, 'Correto?')
    
    try:
        if (message.text == 'Sim'):
            bot.register_next_step_handler(msg, process_curriculum_step)
        else:
            bot.register_next_step_handler(msg, process_fullname_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')
    

def process_curriculum_step(message):
    try:
        chat_id = message.chat.id
        # sex = message.text
        user = user_dict[chat_id]
        # if (sex == u'Male') or (sex == u'Female'):
        #     user.sex = sex
        # else:
        #     raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Prazer em conheçe-lo ' + user.fullname + 
                         '\n Agora daremos andamento ao processo.'+ 
                         ' Criaremos uma pasta no nosso drive com o seu nome e o seu email, para que você possamos gerenciar o processo.\n' +
                         "A partir de agora vamos precisar que voce faça o upload de alguns arquivos começando pelo seu currículo, (vá até o ícone de anexo abaixo e escolha o arquivo do seu currículo para iniciar o upload)")    
        
    except Exception as e:
        bot.reply_to(message, 'oooops')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()