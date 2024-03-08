import requests
from transformers import AutoTokenizer
from pprint import pprint


URL = 'http://localhost:1234/v1/chat/completions'
HEADERS = {"Content-Type": "application/json"}
MAX_TOKENS = 35


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
    user_request = input("Введите запрос к GPT: ")
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


def start():
    menu = {
        "1": {
            "text": "Запрос к GPT",
            "func": send_request
        },
        "2": {
            "text": "Выход",
            "func": end
        }
    }

    print("Добро пожаловать в Чат-с-GPT")
    while True:
        print("Меню:")
        for num, item in menu.items():
            print(f"{num}. {item['text']}")

        choice = input("Выберите: ")
        while choice not in menu:
            choice = input("Выберите корректный пункт: ")

        menu[choice]['func']()


if __name__ == "__main__":
    start()