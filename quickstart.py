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
import time 
# from markup import getMarkup



# telegram bot
# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg") 

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# TODO:
# persist user data
# theme color for bot messages (blue, green, red, etc) 

user_dict = {}
class User:
    def __init__(self):
        self.fullname = None
        self.age = None
        self.sex = None

user = User()

global isFileCreated
isFileCreated = False

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
        user.fullname = fullname
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'Informe seu email:')
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
        bot.register_next_step_handler(msg, process_curriculum_step)
            
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu email")


def process_curriculum_step(message):
    
    try:
        chat_id = message.chat.id
        print('message.text: ', message.text)
        # sex = message.text
        user = user_dict[chat_id]
        
        if(message.text == "Sim"):
            bot.send_message(chat_id, 'Prazer em conheçe-lo ' + user.fullname + 
                            '\n Agora daremos andamento ao processo.')                             
            bot.send_message(chat_id, 'Criaremos uma pasta no nosso drive com o seu nome e o seu email, para que você possamos gerenciar o processo.')
            bot.send_message(chat_id, "A partir de agora vamos precisar que voce faça o upload de alguns arquivos começando pelo seu currículo, vamos lá?")
            msg = bot.send_message(chat_id, 'Vá até o ícone de anexo abaixo e escolha o arquivo do seu currículo para iniciar o upload')
            bot.register_next_step_handler(msg, process_upload_file_step)
            return
        
        elif(message.text == "Não"):
            msg = bot.reply_to(message, 'Ok')
            time.sleep(2)
            bot.register_next_step_handler(msg, process_fullname_step) 
            return         
        
    except Exception as e:
        bot.reply_to(message, 'Erro ao processar o seu currículo: ' + str(e))

# Handle '/upload'
def process_upload_file_step(message):
    bot.send_message(message.chat.id, 'Vamos lá, vamos lá!')
    create_folder_in_googledrive()
    if (isFileCreated):
        bot.send_message(message.chat.id, 'Arquivo criado com sucesso!')
    else:
        bot.send_message(message.chat.id, 'Erro ao criar o arquivo!')
    
    

def create_folder_in_googledrive():
    
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # get the folder id of the user folder in google drive 
        folder_id = '1qwsaMoA2A8vFFPJWgQKp0BY-Gm563c9n' #Pasta: TCC - CHATBOT ENTREVISTA        
                        
        # create a folder inside the user folder        
        folder_name = user.fullname 
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [folder_id]
        }
        file = service.files().create(body=file_metadata,
                                    fields='id').execute()

        print('Folder ID: %s' % file.get('id'))
        isFileCreated = True


        # get file from telegram chat and upload it to google drive
        
        # upload a file
        # file_name = 'test.txt'
        # file_metadata = {
        #     'name': file_name,
        #     'parents': [file.get('id')]            
        # }
        # media = MediaFileUpload(file_name,
        #                         mimetype='text/plain')
        # file = service.files().create(body=file_metadata,
        #                             media_body=media,
        #                             fields='id').execute()
        # print('File ID: %s' % file.get('id'))

        # list files in the user folder 
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print('No files found.')
        else:            
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
            
        
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('\nFiles:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()