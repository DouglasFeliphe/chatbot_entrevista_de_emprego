import requests
import time
import json
import os


class TelegramBot:
    def __init__(self):
        token = '2109357146:AAGRjkbIg0I5gy3kqNV_2G1AWW85xvyahjg'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
      print('Bot rodando...')
      update_id = None
      while True:
        atualizacao = self.obter_novas_mensagens(update_id)
        dados = atualizacao["result"]
        if dados:
          for dado in dados:
              update_id = dado['update_id']
              mensagem = str(dado["message"]["text"])
              chat_id = dado["message"]["from"]["id"]
              eh_primeira_mensagem = int(
                  dado["message"]["message_id"]) == 1
              resposta = self.criar_resposta(
                  mensagem, eh_primeira_mensagem)
              self.responder(resposta, chat_id)
      

    # Obter mensagens
    def obter_novas_mensagens(self, update_id):
      link_requisicao = f'{self.url_base}getUpdates?timeout=100'
      if update_id:
          link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
      resultado = requests.get(link_requisicao)
      return json.loads(resultado.content)

    # Criar uma resposta
    def criar_resposta(self, mensagem, eh_primeira_mensagem):
      if eh_primeira_mensagem == True:
          return f'''Olá bem vindo a nossa lanchonete Digite o número do hamburguer gostaria de pedir:{os.linesep}1 - Queijo MAX{os.linesep}2 - Duplo Burguer Bacon{os.linesep}3 - Triple XXX'''

      if mensagem == 'teste@teste.com':
          return f'''Ótimo! Anotei seu email como {mensagem}. {os.linesep} Está correto? ( sim / não )      
          '''
      # elif mensagem == '2':
      #     return f'''Duplo Burguer Bacon - R$25,00{os.linesep}Confirmar pedido?(s/n)
      #     '''
      # elif mensagem == '3':
      #     return f'''Triple XXX - R$30,00{os.linesep}Confirmar pedido?(s/n)'''

      elif mensagem.lower() in ('s', 'sim'):
          return ''' Agora, informe uma senha de acesso (fique tranquilo nossas mensagens são criptografadas)! '''  

      # elif mensagem == '1e5te':
      #   return f'''Ótimo! Anotei seu email como {mensagem}. {os.linesep} Está correto? ( sim / não )            
                  

      elif mensagem.lower() in ('n', 'não'):
          return ''' Digite novamente seu email: '''
      else:
          return f'Olá, bem vindo ao bot de entrevista!{os.linesep}Ops, esse não parece um email válido. Vamos tentar novamente. Agora informe um email: '

    # Responder
    def responder(self, resposta, chat_id):
      link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
      requests.get(link_requisicao)

bot = TelegramBot()
bot.Iniciar()
