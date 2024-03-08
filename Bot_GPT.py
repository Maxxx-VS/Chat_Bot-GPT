import telebot
from telebot import types
import API


bot = telebot.TeleBot('6547363557:AAGANK3kV2ywllU3LAAXzO7AxIUrtiHj0G0')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋🏻")
    mess = f'Привет, <b>{message.from_user.first_name}!</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html')


    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("START CHAT_GPT 5.0", callback_data="start")
    btn_2 = types.InlineKeyboardButton("STOP CHAT_GPT 5.0", callback_data="stop")
    markup.row(btn_1, btn_2)

    btn_3 = types.InlineKeyboardButton("GO -> TO -> MY -> GIT", url="https://github.com/Maxxx-VS?tab=repositorie")
    markup.row(btn_3)

    bot.send_message(message.chat.id,"<b><u>ВВЫБИРАЙ, ЧТО БУДЕМ ДЕЛАТЬ: </u></b>", reply_markup=markup, parse_mode='html')

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "start":
        API.start()

    if callback.data == "stop":
        API.end()










bot.polling(none_stop=True)