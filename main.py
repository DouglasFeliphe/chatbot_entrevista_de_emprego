from __future__ import print_function
from msilib.schema import MIME

import os
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
from googledrive_api_services import create_user_folder, upload_file_in_user_folder, upload_video_in_user_folder 

from text_services import save_question_in_file, save_answer_in_file
# from markup import getMarkup

# telegram bot
# You can set parse_mode by default. HTML or MARKDOWN
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN) 

# TODO:
# persist user data (curriculum, audio, video, etc)
# cancel process by /cancel command
# human verification
# theme color for bot messages (blue, green, red, etc) 

user_dict = {}
class User:
    def __init__(self):
        self.fullname = None
        self.age = None
        self.sex = None
        self.folder_id = None

user = User()

# Handle '/start' and '/help'
@bot.message_handler(commands=['iniciar'])
def send_welcome(message):
    question = 'Ola, Eu sou o EntrevBot.\nInforme seu nome completo:'    
    
    msg = bot.reply_to(message, question)    
    save_question_in_file(question)
    bot.register_next_step_handler(msg, process_fullname_step)


@bot.message_handler(commands=['cancelar'])
def cancel(message):
    print('cancelar')
    bot.reply_to(message, 'O processo da entrevista foi cancelado.')
    bot.stop_polling()
    bot.stop_bot()
    bot.close()

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        fullname = message.text
        user.fullname = fullname
        user_dict[chat_id] = user
        save_answer_in_file(fullname)
        msg = bot.reply_to(message, 'Informe seu email:')
        save_question_in_file('Informe seu email:')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu nome")


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
        msg = bot.reply_to(message, f'Seu email é {user.email}?', reply_markup=markup)       
        bot.register_next_step_handler(msg, process_get_files_step)
            
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu email")


def process_get_files_step(message):
    
    try:
        chat_id = message.chat.id
        print('message.text: ', message.text)
        # sex = message.text
        user = user_dict[chat_id]
        
        if(message.text == "Sim"):
            save_answer_in_file(user.email)
            bot.send_message(chat_id, 'Prazer em conheçe-lo ' + user.fullname + 
                            '\n Agora daremos andamento ao processo.')  
            
            msg = bot.send_message(chat_id, 'Criaremos uma pasta no nosso drive com o seu nome e o seu email, para que você possamos gerenciar o processo.')
            
            # TODO
            # confirm or cancel user folder creation
            
            bot.register_next_step_handler(msg, process_create_user_folder_step)
            return
        
        elif(message.text == "Não"):
            msg = bot.reply_to(message, 'Ok')
            time.sleep(2)
            bot.register_next_step_handler(msg, process_fullname_step) 
            return         
        
    except Exception as e:
        bot.reply_to(message, 'Erro ao processar o seu currículo: ' + str(e))


# Handle create user folder
def process_create_user_folder_step(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Criando pasta no nosso drive...')
        
    # create user folder in google drive
    user.folder_id = create_user_folder(user.fullname)
    bot.send_message(chat_id, 'Pasta criada com sucesso!') 
    time.sleep(2)
        
    bot.send_message(chat_id, "A partir de agora vamos precisar que voce faça o upload de alguns arquivos começando pelo seu currículo, vamos lá?")
    msg = bot.send_message(chat_id, 'Vá até o ícone de anexo abaixo e escolha o arquivo do seu currículo para iniciar o upload')    
    bot.register_next_step_handler(msg, process_upload_file_step)

# Handle '/document upload'
@bot.message_handler(content_types=['document'])
def process_upload_file_step(message): 
    
    bot.send_message(message.chat.id, 'Fazendo upload do arquivo, aguarde...')
    
    # get file data from message
    filename = message.document.file_name    
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    
    #upload file to google drive user folder   
    doc = message.document    
    upload_file_in_user_folder(filename, user.folder_id, doc)
    bot.send_message(message.chat.id, 'Currículo recebido com sucesso!')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
    time.sleep(2)
    msg = bot.send_message(message.chat.id, 'para conhecer mais sobre o seu perfil gostaríamos que voce enviasse um audio curto sobre voce (max 60 segundos)')
    bot.register_next_step_handler(msg, process_upload_voice_step)

# Handle '/audio/video upload'
@bot.message_handler(content_types=['voice'])
def process_upload_voice_step(message):
    bot.send_message(message.chat.id, 'Fazendo upload do audio, aguarde...')
    
    file_info = bot.get_file(message.voice.file_id)
    
    filename ='apresentacao.ogg'
    
    downloaded_file = bot.download_file(file_info.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    
    #upload file to google drive user folder   
    voice = message.voice    
    upload_file_in_user_folder(filename, user.folder_id, voice)
    
    bot.send_message(message.chat.id, 'Audio recebido com sucesso!')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
    msg = bot.send_message(message.chat.id, 'para conhecer mais sobre o seu perfil gostaríamos que voce enviasse um video curto sobre voce (max 60 segundos)')
    bot.register_next_step_handler(msg, process_upload_video_step)
    
    


@bot.message_handler(content_types=['video_note'])
def process_upload_video_step(message):
    bot.send_message(message.chat.id, 'Fazendo upload do vídeo, aguarde...')
    
    file_info = bot.get_file(message.video_note.file_id)
    
    filename ='apresentacao_video.mkv'
    MIME_TYPE = 'video/x-matroska'
    
    downloaded_file = bot.download_file(file_info.file_path)
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    
    #upload file to google drive user folder  
    upload_video_in_user_folder(filename, user.folder_id, MIME_TYPE)
    
    bot.send_message(message.chat.id, 'Vídeo recebido com sucesso!')
    time.sleep(2)
    # bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
    # msg = bot.send_message(message.chat.id, 'para conhecer mais sobre o seu perfil gostaríamos que voce enviasse um video curto sobre voce (max 60 segundos)')
    # bot.register_next_step_handler(msg, process_upload_audio_step)    
     





# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()