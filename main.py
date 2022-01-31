from __future__ import print_function
from msilib.schema import MIME

import os
import telebot
from telebot import types
import time
from googledrive_api_services import create_user_folder, upload_file_in_user_folder, upload_video_in_user_folder 
from pyairtable import Table

# telegram bot
# You can set parse_mode by default. HTML or MARKDOWN
# BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_TOKEN="2109357146:AAF3t9eP-sC1zIR4dTmDUmxHliC39YVzFvc"
bot = telebot.TeleBot(BOT_TOKEN) 

# airtable API 
AIRTABLE_API = 'keyYlXBzAYqHcwAy8'
AIRTABLE_BASE_ID = 'appQij9zHD2NJ15HZ'
table_participantes = Table(AIRTABLE_API, AIRTABLE_BASE_ID, 'Participantes')
table_vagas = Table(AIRTABLE_API, AIRTABLE_BASE_ID, 'Vagas')

# TODO:
# persist user data (curriculum, audio, video, etc)
# cancel process by /cancel command
# human verification
# theme color for bot messages (blue, green, red, etc) 

user_dict = {}
class User:
    def __init__(self):
        self.fullname = None
        self.desired_job = None
        self.age = None
        self.email = None
        self.cep = None
        self.linkedin = None
        self.curriculum_file_id = None
        self.video_presentation_file_id = None
        self.certifications_file_id = None
        self.three_things = None
        self.hard_decision = None
        self.best_partner = None
        self.future = None
        self.reason = None
        self.status = "Em andamento"
        
        

user = User()

yes_no_markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            resize_keyboard=True
            )       
yes_no_markup.add("Sim","Não")

jobs_markup = types.ReplyKeyboardMarkup(
     one_time_keyboard=True, 
            resize_keyboard=True
        ) 

confirm_cancel_markup = types.ReplyKeyboardMarkup(
                one_time_keyboard=True, 
                resize_keyboard=True
            )       
confirm_cancel_markup.add("Prosseguir","Cancelar")



# Handle '/start' and '/help'
@bot.message_handler(commands=['iniciar'])
def send_welcome(message):
    question = 'Ola, Eu sou o EntrevBot.\nInforme seu nome completo:'   
    msg = bot.reply_to(message, question)  
     
    # save_question_in_file(question)
    bot.register_next_step_handler(msg, process_fullname_step)


@bot.message_handler(commands=['cancelar'])
def cancel_process(message):
    print('cancelar')
    bot.clear_step_handler_by_chat_id(message.chat.id)
    bot.reply_to(message, 'O processo da entrevista foi cancelado.')
    bot.stop_polling()    
    bot.stop_bot()
    bot.close()



def process_fullname_step(message):
    
    # list all jobs and print in keyboard
    for vaga in table_vagas.all(sort=['id']):
        jobs_markup.add(vaga["fields"]["nome"])
         
    try:
        chat_id = message.chat.id
        user.fullname = message.text
        print('message.text', message.text)
        user_dict[chat_id] = user
        msg = bot.send_message(message, 'Informe a vaga desejada:', reply_markup=jobs_markup)
        bot.register_next_step_handler(msg, process_desired_job_step)
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar a vaga desejada")
        
        
         
def process_desired_job_step(message):
    try:        
        chat_id = message.chat.id
        
        # get the job name by id
        
        
        
        user.desired_job = message.text
        print('message.text', message.text)
        user_dict[chat_id] = user
        msg = bot.send_message(message, 'Informe sua idade:')
        bot.register_next_step_handler(msg, process_age_step)
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu nome")



def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        print('message.text', message.text)
        
        if not age.isdigit() and not int(age) > 0:
            msg = bot.reply_to(message, 'Idade inválida. Informe novamente:')
            bot.register_next_step_handler(msg, process_age_step)
            return 
        
        user.age = int(age)
        user_dict[chat_id] = user
        msg = bot.send_message(message, 'Informe seu CEP:')
        bot.register_next_step_handler(msg, process_cep_step)
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar sua idade")


def process_cep_step(message):
    try:
        CEP = message.text
        print('message.text', message.text)
        
        if not CEP.isdigit() and not len(CEP) == 8:
            msg = bot.reply_to(message, 'CEP inválido. Informe novamente:')
            bot.register_next_step_handler(msg, process_cep_step)
            return 
        
        user.cep = int(CEP)
        msg = bot.send_message(message, f'Seu CEP é {CEP}?', reply_markup=yes_no_markup)         
        bot.register_next_step_handler(msg, process_cep_confirm_step)
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu CEP")
 
        
def process_cep_confirm_step(message):
    try:
        if(message.text == 'Sim'):
            msg = bot.send_message(message, 'Informe seu email:')
            bot.register_next_step_handler(msg, process_email_step)
        elif(message.text == "Não"):
            msg = bot.reply_to(message, 'Ok')
            time.sleep(2)
            bot.register_next_step_handler(msg, process_fullname_step) 
            return  
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu CEP")
    


def process_email_step(message):
    try:
        email = message.text
        
        if email.isdigit() or '@' not in email:
            msg = bot.reply_to(message, 'O email que voce digitou é inválido. Informe um email válido:')
            bot.register_next_step_handler(msg, process_email_step)
            return
        
        user.email = email
        msg = bot.send_message(message, f'Seu email é {user.email}?', reply_markup=yes_no_markup)       
        bot.register_next_step_handler(msg, process_linkedin_step)
            
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu email")
        
     
     
def process_linkedin_step(message):
    try:
        if(message.text == 'Sim'):
            msg = bot.send_message(message, 'Informe seu linkedin:')
            user.linkedin = message.text            
            bot.register_next_step_handler(msg, process_linked_confirm_step)
        elif(message.text == "Não"):
            msg = bot.reply_to(message, 'Ok')
            time.sleep(2)
            bot.register_next_step_handler(msg, process_email_step) 
            return 
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar seu email")   
   
   
def process_linked_confirm_step(message):
    try:
        linkedin = message.text
        
        if linkedin.isdigit() or '@' not in linkedin:
            msg = bot.reply_to(message, 'O email que voce digitou é inválido. Informe um email válido:')
            bot.register_next_step_handler(msg, process_email_step)
            return
        
        user.linkedin = linkedin        
        msg = bot.send_message(message, f'Seu linkedin é {user.email}?', reply_markup=yes_no_markup)       
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
           
            bot.send_message(chat_id, 'Prazer em conheçe-lo ' + user.fullname + 
                            '\n Agora daremos andamento ao processo.')  
            
            
            # confirm or cancel user folder creation
            msg = bot.send_message(chat_id, 'Salvaremos as suas informações para que possamos gerenciar o processo.', reply_markup=confirm_cancel_markup)
            
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
    print('Criando pasta no nosso drive...')
    # bot.send_message(chat_id, 'Criando pasta no nosso drive...')
        
    # create user folder in google drive
    user.folder_id = create_user_folder(user.fullname)
    print('Pasta criada com sucesso!')
    # bot.send_message(chat_id, 'Pasta criada com sucesso!') 
    # time.sleep(2)
        
    bot.send_message(chat_id, "A partir de agora vamos precisar que voce faça o upload de alguns arquivos começando pelo seu currículo, vamos lá?")
    time.sleep(2)
    msg = bot.send_message(chat_id, 'Vá até o ícone de anexo abaixo e escolha o arquivo do seu currículo para iniciar o upload')    
    bot.register_next_step_handler(msg, process_upload_curriculum_step)

# Handle '/document upload'
@bot.message_handler(content_types=['document'])
def process_upload_curriculum_step(message): 
    
    bot.send_message(message.chat.id, 'Fazendo upload do arquivo, aguarde...')
    
    # get file data from message
    filename = message.document.file_name    
    file_info = bot.get_file(message.document.file_id)    
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)

    # table.create({"nome_completo": user.fullname, "idade": user.age ,"email": user.email, "curriculum": [{ "filename": 'curriculum.pdf',"url": file_info.file_path }]})
    
    #upload file to google drive user folder   
    doc = message.document    
    user.curriculum_file_id = upload_file_in_user_folder(filename, user.folder_id, doc)
    # user.curriculum_file_id = 
    print(f"curriculum_file_id: {user.curriculum_file_id}",)
    
    bot.send_message(message.chat.id, 'Currículo recebido com sucesso!')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
    time.sleep(2) 
    
    msg = bot.send_message(message.chat.id, 'para conhecer mais sobre o seu perfil gostaríamos que voce enviasse um vídeo curto sobre voce (max 60 segundos)')
    bot.register_next_step_handler(msg, process_upload_video_step)

# Handle '/audio/video upload'
# @bot.message_handler(content_types=['voice'])
# def process_upload_voice_step(message):
#     bot.send_message(message.chat.id, 'Fazendo upload do audio, aguarde...')
    
#     file_info = bot.get_file(message.voice.file_id)
    
#     filename ='apresentacao.ogg'
    
#     downloaded_file = bot.download_file(file_info.file_path)
#     with open(filename, 'wb') as new_file:
#         new_file.write(downloaded_file)

    
#     #upload file to google drive user folder   
#     # voice = message.voice    
#     # upload_file_in_user_folder(filename, user.folder_id, voice)
    
#     bot.send_message(message.chat.id, 'Audio recebido com sucesso!')
#     time.sleep(2)
#     bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
#     msg = bot.send_message(message.chat.id, 'para conhecer mais sobre o seu perfil gostaríamos que voce enviasse um video curto sobre voce (max 60 segundos)')
#     bot.register_next_step_handler(msg, process_upload_video_step)
    


# Handle '/document upload'



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
    user.video_presentation_file_id = upload_video_in_user_folder(filename, user.folder_id, MIME_TYPE)
    
    bot.send_message(message.chat.id, 'Vídeo recebido com sucesso!')
    time.sleep(2)
    bot.send_message(message.chat.id, 'Agora vamos para o próximo passo, vamos lá?')
    msg = bot.send_message(message.chat.id, 'quais são as três coisas mais importantes para voce no seu trabalho?')
    bot.register_next_step_handler(msg, process_three_things_step)    
     


def process_three_things_step(message):
    try:
        chat_id = message.chat.id
        user.three_things = message.text
        bot.send_message(chat_id, 'Ok!')
        time.sleep(2)
        msg = bot.send_message(chat_id, 'Conte-nos qual foi a decisão mais difícil que você teve que tomar nos últimos seis meses?')
        bot.register_next_step_handler(msg, process_hard_decision_step)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_three_things_step)


def process_hard_decision_step(message):
    try:
        chat_id = message.chat.id
        user.hard_decision = message.text
        time.sleep(2)
        msg = bot.send_message(chat_id, 'Descreva o melhor parceiro ou supervisor com quem você já trabalhou e o que considera que era tão interessante no estilo de gestão dessa pessoa?')
        bot.register_next_step_handler(msg, process_best_partner_step)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_hard_decision_step)


def process_best_partner_step(message):
    try:
        chat_id = message.chat.id
        user.best_partner = message.text
        time.sleep(2)
        msg = bot.send_message(chat_id, 'O que acha que vai estar fazendo a esta hora neste mesmo dia, no próximo ano?')
        bot.register_next_step_handler(msg, process_future_step)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_best_partner_step)


def process_future_step(message):
    try:
        chat_id = message.chat.id
        user.future = message.text
        time.sleep(2)
        msg = bot.send_message(chat_id, 'Finalmente, porque você acha que devemos contratá-lo(a)?')
        bot.register_next_step_handler(msg, process_reason_step)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_future_step)


def process_reason_step(message):
    try:
        chat_id = message.chat.id
        user.reason = message.text
        time.sleep(2)
        msg = bot.send_message(chat_id, 'Obrigado!')
        bot.register_next_step_handler(msg, process_end_step)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_reason_step)


def process_end_step(message):
    try:
        chat_id = message.chat.id
         # make a post request to airtable to save the user data
        table_participantes.create({
            "nome_completo": user.fullname, 
            "vaga": user.desired_job,
            "idade": user.age,
            'CEP': user.cep,
            "email": user.email, 
            "linkedin": user.linkedin, 
            "curriculum": [
                {                        
                    "url":f'https://drive.google.com/u/1/uc?id={user.curriculum_file_id}&export=download',
                }                    
            ],
            "video_de_apresentacao": [
                {                        
                    "url":f'https://drive.google.com/u/1/uc?id={user.video_presentation_file_id}&export=download',
                }                    
            ],
            "tres_coisas_importantes" : user.three_things,
            "decisao_dificil" : user.hard_decision,
            "parceiro_ou_supervisor" : user.best_partner,
            "proximo_ano" : user.future,
            "motivo_para_contratar" : user.reason,            
            "status_participacao": user.status, 
            })  
        bot.send_message(chat_id, 'Ok, chegamos ao fim. Agradecemos a sua participação no nosos processo. Obrigado!')
        time.sleep(2)        
        bot.send_message(chat_id, 'O resultado da sua entrevista sairá muito em breve. Voce receberá um email de notificação, fique atento na sua caixa de spam.')
        time.sleep(2)
        bot.send_message(chat_id, 'Boa sorte e até mais!')
        # bot.send_dice(chat_id, emoji='HAPPY_EMOJI')
        # bot.send_animation(chat_id, open('animation.gif', 'rb'))
        # time.sleep(2)
        # bot.send_message(chat_id, 'Você pode acessar seu perfil no menu acima.')
        # time.sleep(2)

    except Exception as e:
        bot.send_message(message.chat.id, 'Desculpe, não entendi o que você quis dizer. Por favor, tente novamente.')
        bot.register_next_step_handler(message, process_end_step)




# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()