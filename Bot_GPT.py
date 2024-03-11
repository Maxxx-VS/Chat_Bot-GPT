import telebot
from telebot import types
import requests
from transformers import AutoTokenizer

URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}
MAX_TOKENS = 35
bot = telebot.TeleBot('6547363557:AAGANK3kV2ywllU3LAAXzO7AxIUrtiHj0G0')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋🏻")
    mess = (f'Привет, <b>{message.from_user.first_name}!\n'
            f'Введи свой запрос к GPT: </b>')
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    global received_text
    received_text = message.text
    print(received_text)
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton("Отправить", callback_data="launch")
    btn_2 = types.InlineKeyboardButton("Вывести ответ", callback_data="answer")
    btn_3 = types.InlineKeyboardButton("GO -> TO -> MY -> GIT", url="https://github.com/Maxxx-VS?tab=repositorie")
    markup.row(btn_1, btn_2)
    markup.row(btn_3)
    bot.send_message(message.chat.id, f"Отправить запрос: <b><u> {received_text} </u></b>?", reply_markup=markup,
                     parse_mode='html')


def answers(message):
    bot.send_message(message.chat.id, f"{content_response}")

    # bot.send_message(message.chat.id, 'И тебе hello')
    # bot.register_next_step_handler(message, text)

    # btn_2 = types.InlineKeyboardButton("STOP CHAT_GPT 5.0", callback_data="stop")
    # markup.row(btn_1, btn_2)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "launch":
        send_request()
    if callback.data == "stop":
        end()
    if callback.data == "answer":
        answers()

def count_tokens(text):
    tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.1")  # название модели
    return len(tokenizer.encode(text))

def make_promt(user_request):
    json = {
        "messages": [
            {
                "role": "user",
                "content": user_request
            },
        ],
        "temperature": 1.2,
        "max_tokens": 200,
    }
    return json

def process_resp(response):
    if response.status_code < 200 or response.status_code >= 300:
        print(f"Ошибка: {response.status_code}")
        return False
    try:
        full_response = response.json()
    except:
        print("Ошибка получения JSON")
        return False

    if "error" in full_response:
        print(f"Ошибка: {full_response['error']}")
        return False
    return full_response

def send_request():
    global content_response
    user_request = received_text
    request_tokens = count_tokens(user_request)
    while request_tokens > MAX_TOKENS or request_tokens < 1:
        user_request = input("Запрос несоответствует кол-ву токенов\nИсправьте запрос: ")
        request_tokens = count_tokens(user_request)
    json = make_promt(user_request)
    resp = requests.post(url=URL, headers=HEADERS, json=json)
    full_response = process_resp(resp)
    if not full_response:
        print("Не удалось выполнить запрос...")
        return False
    content_response = full_response['choices'][0]['message']['content']
    print(content_response)

def end():
    print("До новых встреч!")
    exit(0)

bot.polling(none_stop=True)