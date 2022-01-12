from telebot import types

def getMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Sim')
    btn2 = types.KeyboardButton('Não')  
    markup.add(btn1, btn2)
    return markup
