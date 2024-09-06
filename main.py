import telebot
from telebot import types
import time

bot = telebot.TeleBot(token="7516439034:AAF59uroLK2LSSrcTjHeT5oWZ05stCazCJw")

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    itembtn_str1 = types.KeyboardButton('Финансовый')
    itembtn_str2 = types.KeyboardButton('Тревел')
    itembtn_str3 = types.KeyboardButton('Авто')
    markup.add(itembtn_str1, itembtn_str2, itembtn_str3)
    bot.send_message(message.chat.id, "Пожалуйста выберите необходимый инструмент.", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Финансовый")
def finance(message):
    """
    a lot of code here
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, 'Здравсвуйте, чем я могу вам помочь?')

@bot.message_handler(func=lambda message: message.text == "Тревел")
def travel(message):
    """
    a lot of code here
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, 'Здравсвуйте, чем я могу вам помочь?')

@bot.message_handler(func=lambda message: message.text == "Авто")
def auto(message):
    """
    a lot of code here
    :param message:
    :return:
    """
    bot.send_message(message.chat.id, 'Здравсвуйте, чем я могу вам помочь?')


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        time.sleep(15)
